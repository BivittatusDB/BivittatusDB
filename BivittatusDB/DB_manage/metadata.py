import BivittatusDB as bdb
from DB_manage.funtions.common.list_dir_pydb import list_pydb
from DB_manage.funtions.common.user_interaction_common import get_db_choice
from bdb_aggregate import delay, pause_and_clean

def load_db_and_table(db_directory, table_name):
    try:
        db = bdb.database(db_directory).use()
        print("Database initialized correctly.")
        tb1 = db.load_table(table_name)
        print(f"Table '{table_name}' loaded successfully.")
        return db, tb1
    except Exception as e:
        print(f"Error initializing database or loading table: {e}")
        return None, None

def print_metadata():
    db_choice = get_db_choice()
    if db_choice is None:
        return

    db_directory = input("Enter the name of the database directory: ").strip()
    if db_directory.lower() == 'n':
        print("Operation cancelled.")
        delay(0.8)
        return

    try:
        db_directory, tables = list_pydb(db_directory)
        if not tables:
            print("No tables were found or there was an error listing the files.")
            return
    except Exception as e:
        print(f"Error listing files in directory '{db_directory}': {e}")
        return

    while True:
        print("Available tables:", ", ".join(tables))
        table_name = input("Enter the name of the table you want to use (without .pydb extension): ").strip()
        if table_name in tables:
            break
        print(f"Table '{table_name}' was not found. Enter a valid name from the list above.")
        pause_and_clean(0.8)

    db, tb1 = load_db_and_table(db_directory, table_name)
    if db is None or tb1 is None:
        return

    while True:
        pause_and_clean(1.5)
        print("Table metadata:")
        try:
            print(bdb.metadata(tb1))
        except Exception as e:
            print(f"Error displaying table metadata '{table_name}': {e}")
            return

        exit_choice = input("Do you want to exit (y)? ").strip().lower()
        if exit_choice == "y":
            return
        else:
            print("Invalid entry. Please enter 'y' to exit.")
            pause_and_clean(0.8)
