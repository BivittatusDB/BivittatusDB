import time
import BivittatusDB as bdb
import os

def list_database_files(db_directory, extension=".pydb"):
    """
    List all files in the specified database directory with a given extension.
    
    :param db_directory: Path to the database directory.
    :param extension: File extension to filter by.
    :return: List of file names with the specified extension in the database directory.
    """
    try:
        # Get the list of files in the directory
        files = [f for f in os.listdir(db_directory) if f.endswith(extension)]
        return files
    except FileNotFoundError:
        print("The database directory does not exist.")
        return []
    except PermissionError:
        print("You do not have permission to access the directory.")
        return []

def use_table():
    db_directory = input("Enter the name of the database directory: ")

    # List files in the database directory with the .pydb extension
    files = list_database_files(db_directory)
    
    if not files:
        print("There are no files with the .pydb extension in the database directory.")
        return

    print("Files with the .pydb extension in the database directory:")
    for file in files:
        print(file)

    # Load the database
    db = bdb.database("test").use()

    # Choose a table to load
    table_name = input("Enter the name of the table you want to use: ")

    try:
        #By the moment works like this:
        tb1 = db.load_table(table_name)
        print("The current table:")
        print(tb1)
        time.sleep(3)
    except Exception as e:
        print(f"Error loading the table: {e}")

if __name__ == "__main__":
    use_table()
