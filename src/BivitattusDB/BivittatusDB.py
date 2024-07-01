import h5py, json, gzip, getpass
from bdb_aggregate import *
from binascii import hexlify, unhexlify
from BDB_tb import *
from encrypt import File_Enc

class database:
    def __init__(self, database_name:str):
        self.key=getpass.getpass(f"Password for {database_name}: ").encode()
        self.database_name=database_name

    def __del__(self):
        print("encrypting...")
        File_Enc().enc(self.database_name+".pydb", self.key)

    def load_table(self, table_name:str):
        '''load preexisting tables from the database.'''
        try:
            return table(self.database_name, table_name)
        except Exception as e:
            print(f"Error loading table {table_name} from database {self.database_name}: {e}")
            return None

    def init(self):
        '''initiate a new database. returns self to allow shorter code'''
        with h5py.File(self.database_name+".pydb", "w") as outfile:
            outfile.create_dataset("/database", data=hexlify(gzip.compress(json.dumps(self.database_name).encode())))
        return self
    
    def use(self):
        print("decrypting...")
        File_Enc().dec(self.database_name+".pydb", self.key)
        return self

    def make_table(self, name:str, columns:tuple, data_types:tuple, primary:str=None, foreign:str=None):
        '''Make a new table and specify hte name, columns and data types. Optionally assign primary key. Returns the table'''
        if primary not in columns:
            while primary != None:
                raise NameError(f"Can't make unknown column {primary} into a primary key")
        with h5py.File(self.database_name+".pydb", "a") as editfile:
            editfile.create_dataset(f"/{name}", data=hexlify(gzip.compress(json.dumps([columns]).encode())))
            metadata=[("Data", "Type")]
            for column, value in zip(columns, data_types):
                metadata.append((column, value))
            metadata.append(("Primary Key", f"{primary}"))
            metadata.append(("Foreign Key", f"{foreign}"))
            editfile.create_dataset(f"meta_{name}", data=hexlify(gzip.compress(json.dumps(metadata).encode())))
        return self.load_table(name)

