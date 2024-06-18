import binascii, os
from Crypto.Cipher import AES, Blowfish, Salsa20
from Crypto import Random


#Define Aes encryption initilization vectors
class Aes_enc:
    def pad(self,s,block_size):
        return s + b"\0" * (block_size - len(s) % block_size)

    def encrypt(self,message, key, block_size=32):
        message = self.pad(message, block_size)
        iv = Random.new().read(block_size)
        cipher = AES.new(key, AES.MODE_ECB)
        return iv + cipher.encrypt(message)

    def decrypt(self,ciphertext, key, block_size=32):
        iv = ciphertext[:block_size]
        cipher = AES.new(key, AES.MODE_ECB)
        plaintext = cipher.decrypt(ciphertext[block_size:])
        return plaintext.rstrip(b"\0")

    def enc_file(self, filename, passkey):
        with open(filename, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext, passkey)
        enc_hex=binascii.hexlify(enc)
        with open(filename, 'wb',0) as fo:
            fo.write(enc_hex)

    def dec_file(self, filename, passkey):
        with open(filename, 'rb') as fo:
            ciphertext_hex = fo.read()
        ciphertext=binascii.unhexlify(ciphertext_hex)
        dec = self.decrypt(ciphertext, passkey)
        with open(filename, 'wb',0) as fo:
            fo.write(dec)
            fo.flush()
            os.fsync(fo.fileno())

#Define Blowfish encryption using initilization vectors
class Bfs_enc():
    def pad(self,s, block_size):
        return s + b"\0" * (block_size - len(s) % block_size)

    def encrypt(self,message, key, block_size=32):
        message = self.pad(message, block_size)
        iv = Random.new().read(block_size)
        cipher = Blowfish.new(key, Blowfish.MODE_ECB)
        return iv + cipher.encrypt(message)

    def decrypt(self,ciphertext, key, block_size=32):
        iv = ciphertext[:block_size]
        cipher = Blowfish.new(key, Blowfish.MODE_ECB)
        plaintext = cipher.decrypt(ciphertext[block_size:])
        return plaintext.rstrip(b"\0")

    def enc_file(self, filename, passkey):
        with open(filename, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext, passkey)
        with open(filename, 'wb',0) as fo:
            fo.write(enc)

    def dec_file(self, filename, passkey):
        with open(filename, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, passkey)
        with open(filename, 'wb',0) as fo:
            fo.write(dec)
            fo.flush()
            os.fsync(fo.fileno())

#Define Salsa20 encryption using nonce
class Sla_enc():
    def encrypt(self, key, nonce, message):
        Salsa20.block_size=32
        cipher = Salsa20.new(key=key, nonce=nonce)
        ciphertext = cipher.encrypt(message)
        return ciphertext

    def decrypt(self, key, nonce, ciphertext):
        Salsa20.block_size=32
        cipher = Salsa20.new(key=key, nonce=nonce)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext

    def enc_file(self, filename, passkey, nonce):
        with open(filename, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(passkey, nonce, plaintext)
        with open(filename, 'wb',0) as fo:
            fo.write(enc)

    def dec_file(self, filename, passkey, nonce):
        with open(filename, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(passkey,nonce, ciphertext)
        with open(filename, 'wb', 0) as fo:
            fo.write(dec)
            fo.flush()
            os.fsync(fo.fileno())

#Encrypt file in one go
class File_Enc():
    def __init__(self):
        self.sla=Sla_enc()
        self.bfs=Bfs_enc()
        self.aes=Aes_enc()

    def enc(self, filename, passkey):
        passkey, nonce=self.pad_keys(passkey, passkey[::-1])
        self.sla.enc_file(filename,passkey, nonce)
        self.bfs.enc_file(filename, passkey)
        self.aes.enc_file(filename, passkey)

    def dec(self, filename, passkey):
        passkey, nonce=self.pad_keys(passkey, passkey[::-1])
        self.aes.dec_file(filename, passkey)
        self.bfs.dec_file(filename, passkey)
        self.sla.dec_file(filename, passkey, nonce)

    def pad(self, obj, size):
        if len(obj)> size:
            return obj[:size]
        return obj + b"\0" * (size - len(obj) % size)

    def pad_keys(self, passkey, nonce):
        return self.pad(passkey, 32), self.pad(nonce, 8)