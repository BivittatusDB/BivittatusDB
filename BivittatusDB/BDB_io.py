import metaclass
try: 
    from encrypt import *
    import ctypes, os, getpass
    from json import dumps, loads
    from gzip import compress, decompress
    from binascii import hexlify, unhexlify
except:
    raise metaclass.BDBException.ImportError(f"Could not import needed files in {__file__}")


try:
    io_lib = ctypes.CDLL(f"{os.path.dirname(os.path.abspath(__file__))}/lib_bdb.so")
except:
    raise metaclass.BDBException.ImportError(f"Could not find library lib_bdb.so")

class _CHANDLE:
    def __init__(self) -> None:
        pass

    def CreateDatabase(self, databasename: bytes):
        io_lib.CreateDatabase.argtypes = [ctypes.c_char_p]
        io_lib.CreateDatabase(databasename)
    
    def CreateTable(self, databasename:bytes, tablename:bytes, data:bytes):
        io_lib.CreateTable.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ]
        io_lib.CreateTable(databasename, tablename, data)

    def AddMetaData(self, databasename:bytes, tablename:bytes, metadata:bytes):
        io_lib.AddMetaData.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
        io_lib.AddMetaData(databasename, tablename, metadata)

    def ReadTable(self, database:bytes, tablename:bytes, Metadata:bool):
        io_lib.ReadTable.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
        io_lib.ReadTable.restype = ctypes.c_char_p
        return io_lib.ReadTable(database, tablename, Metadata)
    
    def DeleteTable(self, database:bytes, tablename:bytes):
        io_lib.DeleteTable.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        io_lib.DeleteTable(database, tablename)

    def UpdateTable(self, database:bytes, tablename:bytes, data:bytes):
        io_lib.UpdateTable.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
        io_lib.UpdateTable(database, tablename, data)

    def UpdateMetaTable(self, database:bytes, tablename:bytes, metadata:bytes):
        io_lib.UpdateMetaTable.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
        io_lib.UpdateMetaTable(database, tablename, metadata)

    def CheckDataSet(self, database:bytes, tablename:bytes):
        io_lib.CheckDataSet.argtypes = [ctypes.c_char_p]
        io_lib.CheckDataSet.restype=ctypes.c_int
        return bool(io_lib.CheckDataSet(f"./{database.decode()}/{tablename.decode()}".encode()))

class Handler:
    def __init__(self, database_name:str, Encrypted:bool=False) -> None:
        self.CHANDLE=_CHANDLE()
        self.encryptor=RSAFileEncryptor(database_name)
        self.database=database_name
        self.enc=Encrypted
        self.ext=".pydb"

    def init(self):
        self.CHANDLE.CreateDatabase(self.database.encode())
        print("Generating...")
        self.keygen()
        if self.enc:
            self.secure()
        return self

    def use(self):
        if self.enc:
            self.remove_secure()
        return self
    
    def keygen(self):
        key=RSA.generate(4096)
        private_key=key.export_key()
        public_key=key.publickey().export_key()
        with open(f"./{self.database}/public.pem", "wb") as f:
            f.write(public_key)
        with open(f"./{self.database}/private.pem", "wb") as f:
            f.write(private_key)

    def keyload(self):
        with open(f"./{self.database}/private.pem", "rb") as f:
            self.private_key =RSA.import_key(f.read())
        with open(f"./{self.database}/public.pem", "rb") as f:
            self.public_key=RSA.import_key(f.read())

    def pad(self, s, block_size):
        padding_len = block_size - len(s) % block_size
        return s + bytes([padding_len]) * padding_len
    
    def unpad(self, s):
        padding_len=s[-1]
        return s[:-padding_len]

    def secure(self):
        try:
            try:
                self.password
            except:
                self.password=getpass.getpass(f"Enter password for {self.database}: ")
            with open(f"./{self.database}/private.pem", "rb") as f:
                key=f.read()
            key=self.pad(key, 256)
            password=self.pad(self.password.encode(), 32)
            iv=new().read(16)
            cipher=AES.new(password, AES.MODE_CBC, iv)
            ciphertext=hexlify(iv+cipher.encrypt(key))
            with open(f"./{self.database}/private.pem", "wb") as f:
                f.write(ciphertext)
        except:
            raise metaclass.BDBException.EncryptionError("Problem encrypting data")

    def remove_secure(self):
        try:
            try:
                self.password
            except:
                self.password=getpass.getpass(f"Enter password for {self.database}: ")
            with open(f"./{self.database}/private.pem", "rb") as f:
                key=unhexlify(f.read())
            password=self.pad(self.password.encode(), 32)
            block=AES.block_size
            iv = key[:block]
            cipher=AES.new(password, AES.MODE_CBC, iv)
            key=self.unpad(cipher.decrypt(key[block:]))
            with open(f"./{self.database}/private.pem", "w") as f:
                f.write(key.decode())
        except:
            raise metaclass.BDBException.EncryptionError("Problem Decrypting data")

    def CreateTable(self, tablename:str, data:list, metadata:list):
        try:
            data=hexlify(compress(dumps(data).encode()))
            metadata=hexlify(compress(dumps(metadata).encode()))
            self.CHANDLE.CreateTable(self.database.encode(), (tablename+self.ext).encode(), data)
            self.CHANDLE.AddMetaData(self.database.encode(), (tablename+self.ext).encode(), metadata)
            self.encryptor.encrypt_file(f"./{self.database}/{tablename}.pydb")
        except:
            raise metaclass.BDBException.CreationError(f"Problem Creating table {tablename}")

    def DeleteTable(self, tablename:str):
        try:
            self.CHANDLE.DeleteTable(self.database.encode(), (tablename+self.ext).encode())
        except:
            raise metaclass.BDBException.DeletionError(f"Problem deleting table {tablename}")

    def UpdateTable(self, tablename:str, data:list):
        try:
            self.encryptor.decrypt_file(f"./{self.database}/{tablename}.pydb")
            data=hexlify(compress(dumps(data).encode()))
            self.CHANDLE.UpdateTable(self.database.encode(),(tablename+self.ext).encode(), data)
            self.encryptor.encrypt_file(f"./{self.database}/{tablename}.pydb")
        except:
            raise metaclass.BDBException.EditError(f"Error Updating file {tablename}")

    def UpdateMetaTable(self, tablename:str, metadata:list):
        try:
            self.encryptor.decrypt_file(f"./{self.database}/{tablename}.pydb")
            metadata=hexlify(compress(dumps(metadata).encode()))
            self.CHANDLE.UpdateMetaTable(self.database.encode(),(tablename+self.ext).encode(), metadata)
            self.encryptor.encrypt_file(f"./{self.database}/{tablename}.pydb")
        except:
            raise metaclass.BDBException.EditError(f"Error updating metadata for file {tablename}")

    def ReadTable(self, tablename:str):
        try:
            self.encryptor.decrypt_file(f"./{self.database}/{tablename}.pydb")
            data=self.CHANDLE.ReadTable(self.database.encode(), (tablename+self.ext).encode(), False)
            data=loads(decompress(unhexlify(data)).decode())
            self.encryptor.encrypt_file(f"./{self.database}/{tablename}.pydb")
            return data
        except:
            raise metaclass.BDBException.ReadError(f"Error Reading data from {tablename}")
    
    def ReadMetadata(self, tablename:str):
        try:
            self.encryptor.decrypt_file(f"./{self.database}/{tablename}.pydb")
            data=self.CHANDLE.ReadTable(self.database.encode(), (tablename+self.ext).encode(), True)
            data=loads(decompress(unhexlify(data)).decode())
            self.encryptor.encrypt_file(f"./{self.database}/{tablename}.pydb")
            return data
        except:
            raise metaclass.BDBException.ReadError(f"Error reading metadata from {tablename}")
    
    def TableExists(self, tablename:str):
        return self.CHANDLE.CheckDataSet(self.database.encode(), (tablename+self.ext).encode())

if __name__=="__main__":
    hand=Handler("Hello", True).init().use()
    hand.CreateTable("Test", ["Hello World"], [None])
    print("Test table1 exists: {}".format(hand.TableExists("Test")))

    hand.CreateTable("hello_world", ["check"], ["working..."])
    print("Test table2 exists: {}".format(hand.TableExists("hello_world")))
    data=hand.ReadTable("hello_world")
    metadata=hand.ReadMetadata("hello_world")
    print("{}: {}".format(data[0], metadata[0]))

    hand.DeleteTable("Test")
    print("Test table1 deleted: {}".format(not hand.TableExists("Test")))

    hand.UpdateTable("hello_world", ["new check"])
    data=hand.ReadTable("hello_world")
    metadata=hand.ReadMetadata("hello_world")
    print("{}: {}".format(data[0], metadata[0]))
