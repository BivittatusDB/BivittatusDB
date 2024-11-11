from typing import Any
import metaclass
import json

try:
    from bdb_aggregate import *
    from BDB_tb import *
    from BDB_io import Handler
    from bdb_foreign import Foreign_key
    from encryption.key_transition import KeyTransition
except ImportError:
    raise metaclass.BDBException.ImportError(f"Could not import needed files in {__file__}")

class Database:
    def __init__(self, database_name: str, encrypt: bool = False):
        self.database_name = database_name
        self.encrypt = encrypt
        self.is_init = False  # Database initialization not yet performed

    def init(self):
        """Initialising and using the database."""
        self.db = Handler(self.database_name, self.encrypt)  # Initialize the database only when explicitly called
        self.db.init().use()
        self.is_init = True
        return self

    def use(self):
        """Connect and use the existing database."""
        if not self.is_init:
            self.db = Handler(self.database_name, self.encrypt)
            self.db.use()
            self.is_init = True
        return self

    def load_table(self, table_name: str):
        """Load an existing table from the database."""
        if not self.is_init:
            raise metaclass.BDBException.CreationError("Database not initialized. Please initialize before loading data.")
        try:
            return table(self.db, self.database_name, table_name)
        except Exception:
            raise metaclass.BDBException.IOError(f"Error finding table {table_name}")

    def __call__(self, table_name: str) -> Any:
        return self.load_table(table_name)

    def new_table(self, name: str, columns: tuple, data_types: tuple, primary: str = None, foreign: list = None):
        """Create a new table in the database."""
        if primary and primary not in columns:
            raise metaclass.BDBException.KeyError(f"Can't make unknown column {primary} into a primary key")

        metadata = [("Data", "Type")]
        for column, value in zip(columns, data_types):
            metadata.append((column, value.__name__))
        metadata.append(("Primary Key", primary or "None"))
        metadata.append(("Foreign Key", foreign or "None"))
        metadata.append(("Referenced By", ""))

        # Create table with the provided schema
        self.db.CreateTable(name, [columns], metadata)

        # Configure foreign keys
        if foreign:
            if foreign[2] == "PRIMARY":
                foreign[2] = primary
            if self.db.TableExists(foreign[0]):
                ftable = self.load_table(foreign[0])
                fmeta = ftable.__load_metadata__()
                if foreign[1] == "PRIMARY":
                    foreign[1] = fmeta[1].column.pop(-3)  # Adjust the primary key in the referenced table
                foreign[0] = name
                fkey = Foreign_key(*foreign)
                fmeta[1] = (repr(fkey), fmeta[0] == "Referenced By")
        return self.load_table(name)

    def init_from_json(self, jsonfile):
        """Initialise database from a JSON file."""
        with open(jsonfile) as jf:
            data = json.load(jf)

        # Ensure the database is defined in the JSON
        if self.database_name not in data:
            raise metaclass.BDBException.RefError(f"Cannot find {self.database_name} in {jsonfile}")

        tables = data[self.database_name]
        try:
            drop(self.database_name)
        except Exception:
            pass  # Ignore if the database does not exist

        self.init()  # Initialize the database

        # Create tables from the JSON file
        for table_name, table in tables.items():
            foreign_data = table.get("foreign_key", None)
            self.new_table(
                table_name,
                tuple(table["columns"]),
                tuple([eval(dtype) for dtype in table["data_types"]]),
                table.get("primary_key", None),
                foreign_data if foreign_data is None else [val if val != "PRIMARY" else "PRIMARY" for val in foreign_data]
            )
        return self

    def load_from_json(self, jsonfile):
        """Load data into database tables from a JSON file."""
        if not self.is_init:
            raise metaclass.BDBException.CreationError("Database not initialized. Please initialize before loading data.")

        with open(jsonfile) as jf:
            data = json.load(jf)

        for table_name, table_data in data.items():
            tb = self.load_table(table_name)
            types = tb.__load_metadata__()[1].column[:-3]
            default_values = table_data.get("def_val", None)
            
            for i, datatype in enumerate(types):
                datatype = eval(datatype)
                tableData = table_data["data"]
                for row in tableData:
                    row[i] = datatype(row[i])
                    
            for row in table_data["data"]:
                tb += tuple(row)
            tb.__save__()

# Class to share tables
class Share(KeyTransition):
    def __init__(self, database: str) -> None:
        super().__init__(database)
