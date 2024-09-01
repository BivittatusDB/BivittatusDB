import time
import os
import BivittatusDB as bdb
from bdb_aggregate import pause_and_clean

def list_database_files(db_directory, extension=".pydb"):
    """
    List all files in the specified database directory with a given extension.
    
    :param db_directory: Path to the database directory.
    :param extension: File extension to filter by.
    :return: List of file names with the specified extension in the database directory.
    """
    if not os.path.isdir(db_directory):
        print(f"Directory '{db_directory}' does not exist.")
        return []

    try:
        # Get the list of files in the directory
        files = [f for f in os.listdir(db_directory) if f.endswith(extension)]
        return files
    
    except PermissionError:
        print(f"You do not have permission to access the directory '{db_directory}'.")
        return []
    except Exception:
        print(f"An error occurred while listing files: {Exception}")
        return []

def use_table():
    db_directory = input("Enter the name of the database directory: ")

    # List files in the database directory with the .pydb extension
    files = list_database_files(db_directory)
    
    if not files:
        print("There are no files with the .pydb extension in the database directory.")
        pause_and_clean(1.5)
        return

    print("Files with the .pydb extension in the database directory:")
    for file in files:
        print(file)

    # Load the database

    try:
        db = bdb.database(db_directory).use()
    except Exception:
        print(f"Error initializing the database: {Exception}")
        return

    while True:
        # Choose a table to load
        table_name = input("Enter the name of the table you want to use (without .pydb extension): ")

        # Check if the table exists in the directory
        if f"{table_name}.pydb" not in files:
            print(f"Table '{table_name}' not found. Please enter a valid table name from the list above.")
        else:
            try:
                # Attempt to load the table
                tb1 = db.load_table(table_name)
                print("The current table:")
                print(tb1)
                time.sleep(3)
                break  # Exit loop if table is successfully loaded
            except Exception:
                print(f"Error loading the table '{table_name}': {Exception}")
                break  # Exit loop if there is an error

if __name__ == "__main__":
    use_table()
