import metaclass
try:
    from bdb_aggregate import infomessage
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_OAEP, AES
    from Crypto.Random import get_random_bytes
    from Crypto.Util.Padding import pad, unpad
    from Crypto.Protocol.KDF import PBKDF2
    import os
except ImportError as e:
    raise metaclass.BDBException.ImportError(f"ImportError: {e} - Could not import needed files in {__file__}")
except ModuleNotFoundError as e:
    raise metaclass.BDBException.ImportError(f"ModuleNotFoundError: {e} - Could not import needed files in {__file__}")
except Exception as e:
    raise metaclass.BDBException.ImportError(f"Unexpected error: {e} - Could not import needed files in {__file__}")

class RSAFileEncryptor:
    def __init__(self, database):
        self.key_size = 4096
        self.database = database
        self.private_key_file = f"./{self.database}/private.pem"
        self.public_key_file = f"./{self.database}/public.pem"

    def generate_keys(self):
        try:
            key = RSA.generate(self.key_size)
            private_key = key.export_key()
            public_key = key.publickey().export_key()

            os.makedirs(os.path.dirname(self.private_key_file), exist_ok=True)

            with open(self.private_key_file, "wb") as priv_file:
                priv_file.write(private_key)

            with open(self.public_key_file, "wb") as pub_file:
                pub_file.write(public_key)
        except IOError as e:
            raise RuntimeError(f"Error writing key files: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error during key generation: {e}")

    def encrypt_file(self, input_file):
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"The file {input_file} does not exist.")
        
        try:
            with open(self.public_key_file, "rb") as pub_file:
                public_key = RSA.import_key(pub_file.read())
            cipher_rsa = PKCS1_OAEP.new(public_key)

            # Generate symmetric key (AES)
            session_key = get_random_bytes(16)

            # Encrypt the session key with RSA
            encrypted_session_key = cipher_rsa.encrypt(session_key)

            # Encrypt file data with AES
            with open(input_file, "rb") as f:
                file_data = f.read()

            cipher_aes = AES.new(session_key, AES.MODE_CBC)
            encrypted_data = cipher_aes.encrypt(pad(file_data, AES.block_size))

            # Save the encrypted session key and file data
            with open(input_file, "wb") as f:
                f.write(cipher_aes.iv)
                f.write(encrypted_session_key)
                f.write(encrypted_data)
        except (IOError, ValueError) as e:
            raise RuntimeError(f"Error during file encryption: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error during file encryption: {e}")

    def decrypt_file(self, input_file):
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"The file {input_file} does not exist.")
        
        try:
            with open(self.private_key_file, "rb") as priv_file:
                private_key = RSA.import_key(priv_file.read())
            cipher_rsa = PKCS1_OAEP.new(private_key)

            # Read the encrypted session key and file data
            with open(input_file, "rb") as f:
                iv = f.read(16)
                encrypted_session_key = f.read(512)
                encrypted_data = f.read()

            # Decrypt the session key with RSA
            session_key = cipher_rsa.decrypt(encrypted_session_key)

            # Decrypt file data with AES
            cipher_aes = AES.new(session_key, AES.MODE_CBC, iv)
            decrypted_data = unpad(cipher_aes.decrypt(encrypted_data), AES.block_size)

            with open(input_file, "wb") as f:
                f.write(decrypted_data)
        except (IOError, ValueError) as e:
            raise RuntimeError(f"Error during file decryption: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error during file decryption: {e}")

class KeyManager:
    def __init__(self, database_name):
        self.database = database_name
        self.private_key_path = os.path.join(f"./{self.database}", "private.pem")
        self.public_key_path = os.path.join(f"./{self.database}", "public.pem")
        self.private_key = None
        self.public_key = None

        # Load keys if they already exist
        if os.path.exists(self.private_key_path) and os.path.exists(self.public_key_path):
            self.keyload()

    def key_checker(self):
        """Generate RSA keys and store them in the database directory if they do not exist."""
        if os.path.exists(self.private_key_path) and os.path.exists(self.public_key_path):
            infomessage("Keys already exist. Skipping key generation.")
            return

        try:
            key = RSA.generate(4096)
            private_key = key.export_key()
            public_key = key.publickey().export_key()
            os.makedirs(os.path.dirname(self.private_key_path), exist_ok=True)
            
            with open(self.public_key_path, "wb") as f:
                f.write(public_key)
            with open(self.private_key_path, "wb") as f:
                f.write(private_key)
            infomessage("Keys generated and saved.")
        except IOError as e:
            raise RuntimeError(f"Error writing key files: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error during key generation: {e}")

    def keyload(self):
        """Load RSA keys from the database directory."""
        if not os.path.exists(self.private_key_path) or not os.path.exists(self.public_key_path):
            raise FileNotFoundError("Key files do not exist. Please generate keys first.")
        
        try:
            with open(self.private_key_path, "rb") as f:
                self.private_key = RSA.import_key(f.read())
            with open(self.public_key_path, "rb") as f:
                self.public_key = RSA.import_key(f.read())
        except (IOError, ValueError) as e:
            raise RuntimeError(f"Error loading keys: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error during key loading: {e}")

    @staticmethod
    def pad(s, block_size):
        """Pad the input bytes to be a multiple of block_size."""
        padding_len = block_size - len(s) % block_size
        return s + bytes([padding_len]) * padding_len

    @staticmethod
    def unpad(s):
        """Remove padding from the input bytes."""
        padding_len = s[-1]
        return s[:-padding_len]

class EncryptionManager:
    def __init__(self, database, encrypted=False):
        self.database = database
        self.encrypted = encrypted
        self.key_manager = KeyManager(database)

    def init(self):
        """Initialize the database, generate keys, and secure the private key if encryption is enabled."""
        # Example implementation for creating the database handle
        # self.CHANDLE.CreateDatabase(self.database.encode())
        infomessage("info: Generating keys...", end='')
        self.key_manager.key_checker()
        if self.encrypted:
            self.secure("password")  # Use an appropriate password
        return self

    def use(self):
        """Prepare the database for use by removing security if encryption is enabled."""
        if self.encrypted:
            self.remove_secure("password")  # Use an appropriate password
        return self

    def derive_key(self, password, salt, key_len=32):
        """Derive a cryptographic key from a password using PBKDF2."""
        return PBKDF2(password, salt, dkLen=key_len, count=1000000)

    def secure(self, password):
        """Encrypt the private key with a password."""
        if not self.key_manager.private_key:
            raise RuntimeError("Private key not loaded. Cannot encrypt.")

        try:
            with open(self.key_manager.private_key_path, "rb") as f:
                key = f.read()
            
            salt = get_random_bytes(16)
            derived_key = self.derive_key(password, salt)
            iv = get_random_bytes(16)
            cipher = AES.new(derived_key, AES.MODE_CBC, iv)
            padded_key = self.key_manager.pad(key, AES.block_size)
            ciphertext = iv + salt + cipher.encrypt(padded_key)
            
            with open(self.key_manager.private_key_path, "wb") as f:
                f.write(ciphertext)
            infomessage("Private key encrypted.")
        except (IOError, ValueError) as e:
            raise RuntimeError(f"Error encrypting private key: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error during private key encryption: {e}")

    def remove_secure(self, password):
        """Decrypt the private key with a password."""
        if not os.path.exists(self.key_manager.private_key_path):
            raise FileNotFoundError("Encrypted private key file does not exist.")
        
        try:
            with open(self.key_manager.private_key_path, "rb") as f:
                iv = f.read(16)
                salt = f.read(16)
                encrypted_key = f.read()
            
            derived_key = self.derive_key(password, salt)
            cipher = AES.new(derived_key, AES.MODE_CBC, iv)
            decrypted_key = self.key_manager.unpad(cipher.decrypt(encrypted_key))
            
            with open(self.key_manager.private_key_path, "wb") as f:
                f.write(decrypted_key)
            
            self.key_manager.private_key = RSA.import_key(decrypted_key)
            infomessage("Private key decrypted and loaded.")
        except (IOError, ValueError) as e:
            raise RuntimeError(f"Error decrypting private key: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error during private key decryption: {e}")
