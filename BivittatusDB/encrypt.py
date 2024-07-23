import metaclass
try: 
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_OAEP, AES
    from Crypto.Random import get_random_bytes, new
    from Crypto.Util.Padding import pad, unpad
except:
    raise metaclass.BDBException.ImportError(f"Could not import needed files in {__file__}")


class RSAFileEncryptor:
    def __init__(self, database):
        self.key_size = 4096
        self.database = database
        self.private_key_file = f"./{self.database}/private.pem"
        self.public_key_file = f"./{self.database}/public.pem"

    def generate_keys(self):
        key = RSA.generate(self.key_size)
        private_key = key.export_key()
        public_key = key.publickey().export_key()

        with open(self.private_key_file, "wb") as priv_file:
            priv_file.write(private_key)

        with open(self.public_key_file, "wb") as pub_file:
            pub_file.write(public_key)

    def encrypt_file(self, input_file):
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

    def decrypt_file(self, input_file):
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

# Example usage:
if __name__ == "__main__":
    encryptor = RSAFileEncryptor("Hello")
    encryptor.generate_keys()

    # Encrypt the file
    encryptor.encrypt_file("Hello/plainfile.txt")

    # Decrypt the file
    encryptor.decrypt_file("Hello/encryptedfile.bin")
