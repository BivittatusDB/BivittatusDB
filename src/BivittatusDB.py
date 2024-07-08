from bdb_aggregate import *
from BDB_tb import *
from BDB_io import DBio_lib

class database:
    def __init__(self, database_name:str, Encrpyt:bool=False):
        self.database_name=database_name
        self.db=DBio_lib(database_name, Encrpyt)

    def load_table(self, table_name:str):
        '''load preexisting tables from the database.'''
        try:
            return table(self.db, self.database_name, table_name)
        except Exception as e:
            print(f"Error loading table {table_name} from database {self.database_name}: {e}")
            return None
        
    def __del__(self):
        self.db.close_DB()
    
    def New_table(self, name:str, columns:tuple, data_types:tuple, primary:str=None, foreign:str=None):
        '''Make a new table and specify hte name, columns and data types. Optionally assign primary key. Returns the table'''
        if primary not in columns:
            while primary != None:
                raise NameError(f"Can't make unknown column {primary} into a primary key")
        self.db.CreateTable(name, [columns])
        metadata=[("Data", "Type")]
        for column, value in zip(columns, data_types):
            metadata.append((column, value))
        metadata.append(("Primary Key", f"{primary}"))
        metadata.append(("Foreign Key", f"{foreign}"))
        self.db.CreateTable("meta_"+name, metadata)
        return self.load_table(name)