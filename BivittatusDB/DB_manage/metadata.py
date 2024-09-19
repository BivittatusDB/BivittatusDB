import BivittatusDB as bdb
from DB_manage.funtions.common.list_dir_pydb import list_pydb
from DB_manage.funtions.common.user_interaction_common import get_db_choice
from bdb_aggregate import delay, pause_and_clean

def load_db_and_table(db_directory, table_name):
    """
    Initializes the database and loads the specified table.
    
    Args:
        db_directory (str): Name of the database directory.
        table_name (str): Name of the table to load.

    Returns:
        tuple: (database_instance, table_instance) if the table is loaded successfully, (None, None) otherwise.
    """
    try:
        db = bdb.database(db_directory).use()
        print("Database initialised correctly.")
    except Exception as e:
        print(f"Error initialising the database: {e}")
        return None, None

    try:
        tb1 = db.load_table(table_name)
        print(f"Table ‘{table_name}’ loaded successfully.")
        return db, tb1
    except Exception as e:
        print(f"Error loading table ‘{table_name}’: {e}")
        return None, None

def print_metadata():
    """
    Initialises the database, loads a table if chosen, prints the table metadata, and allows you to select other tables or exit the program.
    and allows to select other tables or exit the program.
    """
    # Ask the user if they want to load an existing database
    db_choice = get_db_choice()

    if db_choice is None:
        return  # Exit if the user chose to cancel

    # Request the name of the database directory
    db_directory = input("Enter the name of the database directory: ").strip()
    if db_directory.lower() == 'n':
        print("Operation cancelled.")
        delay(0.8)
        return

    # Retrieve the database directory name and list of tables
    try:
        db_directory, tables = list_pydb(db_directory)
        if db_directory is None or not tables:
            print("No tables were found or there was an error listing the files.")
            return  # Exit if the operation was cancelled or an error occurred
    except Exception as e:
        print(f"Error listing files in directory '{db_directory}': {e}")
        return

    while True:
        print("Available tables:", ", ".join(tables))
        table_name = input("Enter the name of the table you want to use (without .pydb extension): ").strip()

        if table_name not in tables:
            pause_and_clean(0)
            print(f"Table ‘{table_name}’ was not found. Enter a valid name from the list above.")
        else:
            break

    # Load the database and the table
    db, tb1 = load_db_and_table(db_directory, table_name)
    if db is None or tb1 is None:
        return  # Exit if there was an error loading the database or the table

    # Loop to review metadata and decide whether to exit or continue
    while True:
        # Print the table metadata
        print("Table metadata:")
        try:
            print(bdb.metadata(tb1))
        except Exception as e:
            print(f"Error when displaying table metadata '{table_name}': {e}")
            return

        # Ask if the user wants to exit
        exit_choice = input("Do you want to go out (y)? ").strip().lower()

        if exit_choice == "y":
            return
        else:
            print("Invalid entry. Please enter 'y' to exit.")
            pause_and_clean(0.8)
