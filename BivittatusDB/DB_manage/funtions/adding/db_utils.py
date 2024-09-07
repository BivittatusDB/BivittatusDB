import os
import BivittatusDB as bdb
from bdb_aggregate import delay

def list_database_files(db_directory, extension=".pydb"):
    if not os.path.isdir(db_directory):
        print(f"Directory '{db_directory}' does not exist.")
        return []

    try:
        return [f for f in os.listdir(db_directory) if f.endswith(extension)]
    except PermissionError:
        print(f"You do not have permission to access the directory '{db_directory}'.")
        return []
    except Exception as e:
        print(f"An error occurred while listing files: {e}")
        return []

def load_existing_table(db_name, table_name):
    try:
        test_db = bdb.database(db_name).init()
        tb1 = test_db.load_table(table_name)
        print(f"Table '{table_name}' successfully loaded.")
        #delay(1)
        return tb1
    except Exception as e:
        print(f"Error loading table: {e}")
        return None

def create_new_table(db_name, table_name):
    try:
        test_db = bdb.database(db_name).init()
        tb1 = test_db.New_table(
            table_name,
            ("id", "name"),
            (int(), str()),
            "id"
        )
        print("New table created.")
        return tb1
    except Exception as e:
        print(f"Error creating table: {e}")
        return None
