import BivittatusDB as bdb
from DB_manage.funtions.common.list_dir_pydb import list_pydb
from DB_manage.funtions.common.user_interaction_common import get_db_choice
from bdb_aggregate import delay, pause_and_clean

def load_db_and_table(db_directory, table_name):
    """
    Initializes the database and loads the specified table.
    
    Args:
        db_directory (str): The name of the database folder.
        table_name (str): The name of the table to load.
    
    Returns:
        tuple: (database_instance, table_instance) if the table is successfully loaded, (None, None) otherwise.
    """
    try:
        db = bdb.database(db_directory).use()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing the database: {e}")
        return None, None

    try:
        tb1 = db.load_table(table_name)
        print(f"Table '{table_name}' loaded successfully.")
        return db, tb1
    except Exception as e:
        print(f"Error loading the table '{table_name}': {e}")
        return None, None

def print_metadata():
    """
    Initializes the database, loads a table if chosen, prints the table metadata,
    and allows selecting other tables or exiting the program.
    """
    # Ask the user if they want to load an existing database
    db_choice = get_db_choice()
    
    if db_choice is None:
        return  # Exit if the user chose to cancel

    # Request the name of the database folder
    db_directory = input("Enter the name of the database folder: ").strip()
    if db_directory.lower() == 'n':
        print("Operation cancelled.")
        delay(0.8)
        return

    # Retrieve the name of the database folder and the list of tables
    db_directory, tables = list_pydb(db_directory)
    if db_directory is None:
        return  # Exit if the operation was cancelled or an error occurred

    while True:
        print("Available tables:", ", ".join(tables))
        table_name = input("Enter the name of the table you want to use (without .pydb extension): ").strip()

        if table_name not in tables:
            pause_and_clean(0)
            print(f"The table '{table_name}' is not found. Please enter a valid name from the list above.")
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
        print(bdb.metadata(tb1))

        # Ask if the user wants to exit
        exit_choice = input("Do you want to exit (y)? ").strip().lower()
        
        if exit_choice == "y":
            return
        else:
            print("Invalid input. Please enter 'y' to exit")
            pause_and_clean(0.8)
