import os
from bdb_aggregate import infomessage
from traceback import format_exc as trace
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidKey

class KeyManager:
    def __init__(self, database, key_size=4096):
        """
        Initialize KeyManager with the path to the database and RSA key size.
        
        :param database: Path to the directory where keys are stored.
        :param key_size: Size of the RSA key in bits (default is 4096).
        """
        self.key_size = key_size
        self.database = database
        self.private_key_file = os.path.join(self.database, "private.pem")
        self.public_key_file = os.path.join(self.database, "public.pem")
        self.ensure_database_exists()
        self.key_checker()

    def ensure_database_exists(self):
        """Ensure that the database directory exists."""
        if not os.path.exists(self.database):
            try:
                os.makedirs(self.database)
                infomessage(f"Database directory '{self.database}' created.")
            except OSError as e:
                infomessage(f"Error creating database directory: {e}")
                infomessage(trace())
                raise RuntimeError(f"Error creating database directory: {e}")

    def generate_keys(self):
        """Generate RSA key pair and save to files."""
        try:
            key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=self.key_size,
                backend=default_backend()
            )
            private_key = key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()  # Optional: Use BestAvailableEncryption(b"your-password")
            )
            public_key = key.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            os.makedirs(os.path.dirname(self.private_key_file), exist_ok=True)
            with open(self.private_key_file, "wb") as priv_file:
                priv_file.write(private_key)
            with open(self.public_key_file, "wb") as pub_file:
                pub_file.write(public_key)
            infomessage("Keys generated and saved successfully.")
        except IOError as e:
            infomessage(f"IOError during key generation: {e}")
            infomessage(trace())
            raise RuntimeError(f"IOError during key generation: {e}")
        except Exception as e:
            infomessage(f"Unexpected error during key generation: {e}")
            infomessage(trace())
            raise RuntimeError(f"Unexpected error during key generation: {e}")

    def load_public_key(self, pub_key:str=None):
        """Load the public key from file."""
        if pub_key==None:
            if not os.path.exists(self.public_key_file):
                raise FileNotFoundError(f"Public key file '{self.public_key_file}' does not exist.")
            with open(self.public_key_file, "rb") as pub_file:
                return serialization.load_pem_public_key(pub_file.read(), backend=default_backend())
        else:
            if not os.path.exists(pub_key):
                raise FileNotFoundError(f"Public key file '{pub_key}' does not exist.")
            with open(pub_key, "rb") as pub_file:
                return serialization.load_pem_public_key(pub_file.read(), backend=default_backend())


    def load_private_key(self, priv_key:str=None):
        """Load the private key from file."""
        if priv_key==None:
            if not os.path.exists(self.private_key_file):
                raise FileNotFoundError(f"Private key file '{self.private_key_file}' does not exist.")
            with open(self.private_key_file, "rb") as priv_file:
                return serialization.load_pem_private_key(priv_file.read(), password=None, backend=default_backend())
        else:
            if not os.path.exists(priv_key):
                raise FileNotFoundError(f"Private key file '{priv_key}' does not exist.")
            with open(priv_key, "rb") as priv_file:
                return serialization.load_pem_private_key(priv_file.read(), password=None, backend=default_backend())

    def verify_key_pair(self):
        """Verify that the public and private key pair match."""
        private_key = self.load_private_key()
        public_key = self.load_public_key()

        try:
            test_data = b"test"
            encrypted_data = public_key.encrypt(
                test_data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            decrypted_data = private_key.decrypt(
                encrypted_data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            if decrypted_data != test_data:
                raise ValueError("Public and private keys do not match.")
        except (ValueError, TypeError) as e:
            infomessage(f"Key verification failed: {e}")
            infomessage(trace())
            raise RuntimeError(f"Key verification failed: {e}")
        except Exception as e:
            infomessage(f"Unexpected error during key verification: {e}")
            infomessage(trace())
            raise RuntimeError(f"Unexpected error during key verification: {e}")

    def key_checker(self):
        """Check the validity of key files and their pair. Generate keys if missing."""
        try:
            if not (os.path.exists(self.private_key_file) and os.path.exists(self.public_key_file)):
                infomessage("Key files are missing. Generating new keys...")
                self.generate_keys()
            self.verify_key_pair()
            infomessage("Keys are valid and match.")
        except (FileNotFoundError, IOError, ValueError, TypeError) as e:
            infomessage(trace())
            infomessage(f"Key check failed: {e}")
            infomessage("Regenerating keys...")
            self.generate_keys()  # Regenerate keys if validation fails
            self.verify_key_pair()  # Re-verify after regeneration
        except Exception as e:
            infomessage(trace())
            infomessage(f"Unexpected error during key check: {e}")
            raise RuntimeError(f"Unexpected error during key check: {e}")

class RSAFileEncryptor:
    def __init__(self, database):
        """
        Initialize RSAFileEncryptor with the path to the database.
        
        :param database: Path to the directory where keys are stored.
        """
        self.key_manager = KeyManager(database)
        self.public_key = self.key_manager.load_public_key()
        self.private_key = self.key_manager.load_private_key()
        self.database = database

    def generate_keys(self):
        """Delegate key generation to KeyManager."""
        self.key_manager.generate_keys()

    def encrypt_file(self, input_file, output_file:str=None):
        """Encrypt a file using RSA and AES."""
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"The file {input_file} does not exist.")
        if os.path.getsize(input_file) == 0:
            raise ValueError(f"The file {input_file} is empty.")

        try:
            # Generate a symmetric AES key
            session_key = os.urandom(32)

            # Encrypt the session key with RSA
            encrypted_session_key = self.public_key.encrypt(
                session_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            # Encrypt the file data with AES-GCM
            with open(input_file, "rb") as f:
                file_data = f.read()

            iv = os.urandom(12)  # Recommended: 96 bits (12 bytes) for GCM
            cipher = Cipher(algorithms.AES(session_key), modes.GCM(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            encrypted_data = encryptor.update(file_data) + encryptor.finalize()
            output_file = output_file or input_file
            # Save the encrypted session key, IV, tag, and encrypted data
            with open(output_file, "wb") as f:
                f.write(iv)
                f.write(encrypted_session_key)
                f.write(encryptor.tag)  # GCM tag for authentication
                f.write(encrypted_data)
            infomessage("File encrypted successfully.")
        except (IOError, ValueError) as e:
            infomessage(f"Error during file encryption: {e}")
            infomessage(trace())
            raise RuntimeError(f"Error during file encryption: {e}")
        except Exception as e:
            infomessage(f"Unexpected error during file encryption: {e}")
            infomessage(trace())
            raise RuntimeError(f"Unexpected error during file encryption: {e}")

    def decrypt_file(self, input_file):
        """Decrypt a file encrypted using RSA and AES."""
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"The file {input_file} does not exist.")
        if os.path.getsize(input_file) == 0:
            raise ValueError(f"The file {input_file} is empty.")

        try:


            # Read encrypted session key, IV, tag, and encrypted data
            with open(input_file, "rb") as f:
                iv = f.read(12)  # 12 bytes for IV in GCM
                encrypted_session_key = f.read(self.private_key.key_size // 8)
                tag = f.read(16)  # 16 bytes for tag in GCM
                encrypted_data = f.read()

            # Decrypt the session key with RSA
            session_key = self.private_key.decrypt(
                encrypted_session_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            # Decrypt the file data with AES-GCM
            cipher = Cipher(algorithms.AES(session_key), modes.GCM(iv, tag), backend=default_backend())
            decryptor = cipher.decryptor()
            decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

            # Save the decrypted data back to the file
            with open(input_file, "wb") as f:
                f.write(decrypted_data)
            infomessage("File decrypted successfully.")
        except (IOError, ValueError, InvalidKey) as e:
            infomessage(f"Error during file decryption: {e}")
            infomessage(trace())
            raise RuntimeError(f"Error during file decryption: {e}")
        except Exception as e:
            infomessage(f"Unexpected error during file decryption: {e}")
            infomessage(trace())
            raise RuntimeError(f"Unexpected error during file decryption: {e}")

# Example usage
if __name__ == "__main__":
    database = "bivittatusDB/test"  # Database path
    input_file = os.path.join(database, "public.pem")

    encryptor = RSAFileEncryptor(database)

    # Encryption
    try:
        encryptor.encrypt_file(input_file)
        infomessage("File encrypted successfully.")
    except FileNotFoundError as e:
        infomessage(f"Encryption failed: {e}")
        infomessage(trace())
    except Exception as e:
        infomessage(f"Unexpected error during encryption: {e}")
        infomessage(trace())

    # Decryption
    try:
        encryptor.decrypt_file(input_file)
        infomessage("File decrypted successfully.")
    except FileNotFoundError as e:
        infomessage(f"Decryption failed: {e}")
        infomessage(trace())
    except Exception as e:
        infomessage(f"Unexpected error during decryption: {e}")
        infomessage(trace())


class KeyTransition:
    def __init__(self, database:str) -> None:
        self.path=database
        self.rsa=RSAFileEncryptor(self.path)

    def __copy_pubKey__(self):
        with open(f"{self.path}/private.pem", "rb") as original:
            with open(f"{self.path}/key.priv", "wb") as copy:
                copy.write(original.read())

    def ReKey(self, regen:bool=False):
        #used to generate new keys for a database
        if regen==True:
            self.__copy_pubKey__()
            self.rsa.generate_keys()
            self.priv_key=f"{self.path}/key.priv"
            self.rsa.private_key=self.rsa.key_manager.load_private_key(self.priv_key)
            self.rsa.public_key=self.rsa.key_manager.load_public_key()
        for file in os.listdir(self.path):
            if ".pydb" in file:
                self.rsa.decrypt_file(self.path+"/"+file)
                self.rsa.encrypt_file(self.path+"/"+file)
        self.rsa.private_key=self.rsa.key_manager.load_private_key()
    
    def export_table(self, table_name:str, export_key:str):
        "re-encrypt a table with a given public key, so that you don't need to share your private key"
        self.rsa.public_key=self.rsa.key_manager.load_public_key(export_key)
        self.rsa.decrypt_file(f"{self.path}/{table_name}.pydb")
        os.makedirs(f"{self.path}_export", exist_ok=True)
        self.rsa.encrypt_file(f"{self.path}/{table_name}.pydb", f"{self.path}_export/{table_name}.pydb")
        self.rsa.public_key=self.rsa.key_manager.load_public_key()
        self.rsa.encrypt_file(f"{self.path}/{table_name}.pydb")

    def import_table(self, table_path:str, import_key:str):
        'import a table that has been shared with you via Share.export_table, if you are the private key holder'
        _, filename = os.path.split(table_path)
        self.rsa.private_key=self.rsa.key_manager.load_private_key(import_key)
        self.rsa.decrypt_file(table_path)
        self.rsa.encrypt_file(table_path, f"{self.path}/{filename}")
        self.rsa.private_key=self.rsa.key_manager.load_private_key()