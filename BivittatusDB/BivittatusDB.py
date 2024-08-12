import metaclass
try: 
    from bdb_aggregate import *
    from BDB_tb import *
    from BDB_io import Handler
    from bdb_foreign import ForeignKey
except:
    raise metaclass.BDBException.ImportError(f"Could not import needed files in {__file__}")

class database:
    def __init__(self, database_name:str, Encrpyt:bool=False):
        self.database_name=database_name
        self.db=Handler(database_name, Encrpyt)

    def init(self):
        self.db.init().use()
        return self
    
    def use(self):
        self.db.use()
        return self

    def load_table(self, table_name:str):
        '''load preexisting tables from the database.'''
        try:
            return table(self.db, self.database_name, table_name)
        except Exception as e:
            raise metaclass.BDBException.IOError(f"Error finding table {table_name}")
    
    def New_table(self, name:str, columns:tuple, data_types:tuple, primary:str=None, foreign:list=None):
        '''Make a new table and specify the name, columns and data types. Optionally assign primary key. Returns the table'''
        if primary not in columns:
            while primary != None:
                raise metaclass.BDBException.KeyError(f"Can't make unknown column {primary} into a primary key")
        metadata=[("Data", "Type")]
        for column, value in zip(columns, data_types):
            metadata.append((column, value))
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
                FKey=ForeignKey(*foreign)
                fmeta[1]=(repr(FKey), fmeta[0]=="Refrenced By")
        return self.load_table(name)