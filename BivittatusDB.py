import h5py, json
from bdb_aggregate import *
from BDB_tb import *

class database:
    def __init__(self, database_name:str):
        self.database_name=database_name

    def load_table(self, table_name:str):
        '''load preexisting tables from the database.'''
        return table(self.database_name, table_name)
    
    def init(self):
        '''initiate a new database. returns self to allow shorter code'''
        with h5py.File(self.database_name+".pydb", "w") as outfile:
            outfile.create_dataset("/database", data=self.database_name.encode())
        return self

    def make_table(self, name:str, columns:tuple, data_types:tuple, primary:str=None, foreign:str=None):
        '''Make a new table and specify hte name, columns and data types. Optionally assign primary key. Returns the table'''
        if primary not in columns:
            while primary != None:
                raise NameError(f"Can't make unknown column {primary} into a primary key")
        with h5py.File(self.database_name+".pydb", "a") as editfile:
            editfile.create_dataset(f"/{name}", data=json.dumps([columns]))
            metadata=[("Data", "Type")]
            for column, value in zip(columns, data_types):
                metadata.append((column, value))
            metadata.append(("Primary Key", f"{primary}"))
            metadata.append(("Foreign Key", f"{foreign}"))
            editfile.create_dataset(f"meta_{name}", data=json.dumps(metadata))
        return self.load_table(name)

