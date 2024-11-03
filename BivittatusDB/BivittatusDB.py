from typing import Any
import metaclass
try:
    from bdb_aggregate import *
    from BDB_tb import *
    from BDB_io import Handler
    from bdb_foreign import Foreign_key
    from encryption.key_transition import KeyTransition
except:
    raise metaclass.BDBException.ImportError(f"Could not import needed files in {__file__}")

class database:
    def __init__(self, database_name:str, Encrypt:bool=False):
        self.database_name=database_name
        self.Encrypt = Encrypt

    def init(self):
        self.db=Handler(self.database_name, self.Encrypt) #move down to remove pre-mature initialization
        self.db.init().use()
        self.is_init=True
        return self
    
    def use(self):
        self.db=Handler(self.database_name, self.Encrypt)
        self.db.use()
        self.is_init=True
        return self

    def load_table(self, table_name:str):
        '''load preexisting tables from the database.'''
        if not self.is_init:
            raise metaclass.BDBException.CreationError("Database not initialized. please initialize before loading data.")
        try:
            return table(self.db, self.database_name, table_name)
        except Exception:
            raise metaclass.BDBException.IOError(f"Error finding table {table_name}")
    
    def __call__(self, table_name:str) -> table:
        return self.load_table(table_name)

    def New_table(self, name:str, columns:tuple, data_types:tuple, primary:str=None, foreign:list=None):
        '''Make a new table and specify the name, columns and data types. Optionally assign primary key. Returns the table'''
        if primary not in columns:
            while primary != None:
                raise metaclass.BDBException.KeyError(f"Can't make unknown column {primary} into a primary key")
        metadata=[("Data", "Type")]
        for column, value in zip(columns, data_types):
            metadata.append((column, value()))
        metadata.append(("Primary Key", f"{primary}"))
        metadata.append(("Foreign Key", f"{foreign}"))
        metadata.append(("Refrenced By", ""))
        self.db.CreateTable(name, [columns], metadata)
        if foreign != None:
            if foreign[2]==PRIMARY:
                foreign[2]=primary
            if self.db.TableExists(foreign[0]):
                ftable=self.load_table(foreign[0])
                fmeta=ftable.__load_metadata__()
                if foreign[1]==PRIMARY:
                    foreign[1]=fmeta[1].column.pop(-3)
                foreign[0]=name
                FKey=Foreign_key(*foreign)
                fmeta[1]=(repr(FKey), fmeta[0]=="Refrenced By")
        return self.load_table(name)
    
    def init_from_json(self, jsonfile):
        with open(jsonfile) as jf:
            data=dict(json.load(jf))
        
        #ensure the database is defined in the json file
        try:
            tables=data[self.database_name]
        except:
            raise metaclass.BDBException.RefError(f"Cannot find {self.database_name} in {jsonfile}")
        
        #init the database
        try: drop(self.database_name)
        except: pass
        self.init()

        for table in tables.keys():
            tbname, table = table, tables[table]
            foreign_data=table.get("foreign_key", None)
            self.New_table(tbname,
                           tuple(table["columns"]),
                           tuple([eval(type) for type in table["data_types"]]),
                           table.get("primary_key", None),
                           foreign_data if foreign_data==None else [val if val!="PRIMARY" else PRIMARY for val in foreign_data]
                           )
        return self

    def load_from_json(self, jsonfile):
        '''Load table data into the database from json'''
        if not self.is_init:
            raise metaclass.BDBException.CreationError("Database not initialized. please initialize before loading data.")        
        with open(jsonfile) as jf:
            data=dict(json.load(jf))
        for table in data.keys():
            tb=self.load_table(table)
            types=tb.__load_metadata__()[1].column[:-3]
            default=data[table].get("def_val", None)
            for i, datatype in enumerate(types):
                datatype=type(datatype)
                tableData=data[table]["data"]
                for row in tableData:
                    row[i]=datatype(row[i])
            for row in data[table]["data"]:
                tb+tuple(row)
            tb.__save__()

#used for sharing tables
class Share(KeyTransition):
    def __init__(self, database:str) -> None:
        super().__init__(database)