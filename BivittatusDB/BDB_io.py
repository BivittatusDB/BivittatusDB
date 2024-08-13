from encrypt import KeyManager
from bdb_aggregate import infomessage
import metaclass
import ctypes
import os
import getpass
from json import dumps, loads
from gzip import compress, decompress
from binascii import hexlify, unhexlify

# Import encryption-related functionalities
try:
    from encrypt import RSAFileEncryptor
except ImportError:
    raise metaclass.BDBException.ImportError(f"Could not import needed files in {__file__}")

# Load the shared library
def load_shared_library():
    library_name = 'lib_bdb_win32.so' if os.name == 'nt' else 'lib_bdb_elf.so'
    library_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), library_name)
    try:
        return ctypes.CDLL(library_path)
    except OSError as e:
        raise metaclass.BDBException.ImportError(f"Could not load shared library {library_path}: {e}")

io_lib = load_shared_library()

# _CHANDLE class definition
class _CHANDLE:
    def __init__(self):
        pass

    def _call_lib_function(self, func_name, *args, restype=None):
        func = getattr(io_lib, func_name, None)
        if func is None:
            raise AttributeError(f"Function {func_name} not found in shared library")
        
        argtypes = []
        for arg in args:
            if isinstance(arg, bytes):
                argtypes.append(ctypes.c_char_p)
            elif isinstance(arg, int):
                argtypes.append(ctypes.c_int)
            else:
                raise TypeError(f"Unsupported argument type: {type(arg)}")
        func.argtypes = argtypes
        if restype:
            func.restype = restype
        return func(*args)

    def CreateDatabase(self, databasename: bytes):
        self._call_lib_function('CreateDatabase', databasename)

    def CreateTable(self, databasename: bytes, tablename: bytes, data: bytes):
        self._call_lib_function('CreateTable', databasename, tablename, data)

    def AddMetaData(self, databasename: bytes, tablename: bytes, metadata: bytes):
        self._call_lib_function('AddMetaData', databasename, tablename, metadata)

    def ReadTable(self, database: bytes, tablename: bytes, metadata: int):
        result = self._call_lib_function('ReadTable', database, tablename, metadata, restype=ctypes.c_char_p)
        return result

    def DeleteTable(self, database: bytes, tablename: bytes):
        self._call_lib_function('DeleteTable', database, tablename)

    def UpdateTable(self, database: bytes, tablename: bytes, data: bytes):
        self._call_lib_function('UpdateTable', database, tablename, data)

    def UpdateMetaTable(self, database: bytes, tablename: bytes, metadata: bytes):
        self._call_lib_function('UpdateMetaTable', database, tablename, metadata)

    def CheckDataSet(self, database: bytes, tablename: bytes) -> bool:
        result = self._call_lib_function('CheckDataSet', f"./{database.decode()}/{tablename.decode()}".encode(), restype=ctypes.c_int)
        return bool(result)

# Main Handler class
class Handler:
    def __init__(self, database_name: str, encrypted: bool = False) -> None:
        self.CHANDLE = _CHANDLE()
        self.encryptor = RSAFileEncryptor(database_name)
        self.key_manager = KeyManager(database_name)
        self.database = database_name
        self.encrypted = encrypted
        self.ext = ".pydb"

    def init(self):
        """Initialize the database, generate keys, and secure the private key if encryption is enabled."""
        self.CHANDLE.CreateDatabase(self.database.encode())
        infomessage("info: Generating keys...", end='')
        self.key_manager.key_checker()
        if self.encrypted:
            self.secure()
        return self

    def use(self):
        """Prepare the database for use by removing security if encryption is enabled."""
        if self.encrypted:
            self.remove_secure()
        return self

    def secure(self):
        """Secure the private key with a password."""
        password = self._get_password("Enter password to secure the private key: ")
        self.key_manager.secure(password)

    def remove_secure(self):
        """Remove security from the private key with a password."""
        password = self._get_password("Enter password to remove security from the private key: ")
        self.key_manager.remove_secure(password)

    def _get_password(self, prompt: str) -> str:
        """Prompt the user for a password with hidden input."""
        while True:
            password = getpass.getpass(prompt)
            if password:
                return password
            else:
                infomessage("Password cannot be empty. Please try again.", end='')

    def CreateTable(self, tablename: str, data: list, metadata: list):
        """Create a table with the given name, data, and metadata."""
        try:
            data = hexlify(compress(dumps(data).encode()))
            metadata = hexlify(compress(dumps(metadata).encode()))
            table_name = (tablename + self.ext).encode()
            self.CHANDLE.CreateTable(self.database.encode(), table_name, data)
            self.CHANDLE.AddMetaData(self.database.encode(), table_name, metadata)
            self.encryptor.encrypt_file(f"./{self.database}/{tablename}.pydb")
        except Exception as e:
            raise metaclass.BDBException.CreationError(f"Problem creating table {tablename}: {e}")

    def DeleteTable(self, tablename: str):
        """Delete the table with the given name."""
        try:
            self.CHANDLE.DeleteTable(self.database.encode(), (tablename + self.ext).encode())
        except Exception as e:
            raise metaclass.BDBException.DeletionError(f"Problem deleting table {tablename}: {e}")

    def UpdateTable(self, tablename: str, data: list):
        """Update the table with the given name with new data."""
        try:
            self.encryptor.decrypt_file(f"./{self.database}/{tablename}.pydb")
            data = hexlify(compress(dumps(data).encode()))
            self.CHANDLE.UpdateTable(self.database.encode(), (tablename + self.ext).encode(), data)
            self.encryptor.encrypt_file(f"./{self.database}/{tablename}.pydb")
        except Exception as e:
            raise metaclass.BDBException.EditError(f"Error updating table {tablename}: {e}")

    def UpdateMetaTable(self, tablename: str, metadata: list):
        """Update the metadata of the table with the given name."""
        try:
            self.encryptor.decrypt_file(f"./{self.database}/{tablename}.pydb")
            metadata = hexlify(compress(dumps(metadata).encode()))
            self.CHANDLE.UpdateMetaTable(self.database.encode(), (tablename + self.ext).encode(), metadata)
            self.encryptor.encrypt_file(f"./{self.database}/{tablename}.pydb")
        except Exception as e:
            raise metaclass.BDBException.EditError(f"Error updating metadata for table {tablename}: {e}")

    def ReadTable(self, tablename: str):
        """Read the data from the table with the given name."""
        try:
            self.encryptor.decrypt_file(f"./{self.database}/{tablename}.pydb")
            data = self.CHANDLE.ReadTable(self.database.encode(), (tablename + self.ext).encode(), int(False))
            data = loads(decompress(unhexlify(data)).decode())
            self.encryptor.encrypt_file(f"./{self.database}/{tablename}.pydb")
            return data
        except Exception as e:
            raise metaclass.BDBException.ReadError(f"Error reading data from table {tablename}: {e}")

    def ReadMetadata(self, tablename: str):
        """Read the metadata from the table with the given name."""
        try:
            self.encryptor.decrypt_file(f"./{self.database}/{tablename}.pydb")
            metadata = self.CHANDLE.ReadTable(self.database.encode(), (tablename + self.ext).encode(), int(True))
            metadata = loads(decompress(unhexlify(metadata)).decode())
            self.encryptor.encrypt_file(f"./{self.database}/{tablename}.pydb")
            return metadata
        except Exception as e:
            raise metaclass.BDBException.ReadError(f"Error reading metadata from table {tablename}: {e}")

    def TableExists(self, tablename: str) -> bool:
        """Check if the table with the given name exists in the database."""
        return self.CHANDLE.CheckDataSet(self.database.encode(), (tablename + self.ext).encode())

# Example usage
if __name__ == "__main__":
    handler = Handler("Hello", True).init().use()
    
    try:
        handler.CreateTable("Test", ["Hello World"], [None])
        print(f"Test table1 exists: {handler.TableExists('Test')}")

        handler.CreateTable("hello_world", ["check"], ["working..."])
        print(f"Test table2 exists: {handler.TableExists('hello_world')}")
        
        data = handler.ReadTable("hello_world")
        metadata = handler.ReadMetadata("hello_world")
        print(f"{data[0]}: {metadata[0]}")

        handler.DeleteTable("Test")
        print(f"Test table1 deleted: {not handler.TableExists('Test')}")

        handler.UpdateTable("hello_world", ["new check"])
        data = handler.ReadTable("hello_world")
        metadata = handler.ReadMetadata("hello_world")
        print(f"{data[0]}: {metadata[0]}")
    
    except metaclass.BDBException as e:
        infomessage(f"Database operation error: {e}")
