import BivittatusDB as bdb
from DB_manage.list_pydb import list_db_files

def print_pydb_files(db_directory):
    # List files in the database directory with the .pydb extension
    files = list_db_files(db_directory)

    if not files:
        print("There are no files with the .pydb extension in the database directory.")
    else:
        print("Files with the .pydb extension in the database directory:")
        for file in files:
            print(file)
    return files

def use_table():
    # Prompt the user for the name of the database directory
    db_directory = input("Enter the name of the database directory: ").strip()

    # Print available .pydb files in the directory
    files = print_pydb_files(db_directory)
    if not files:
        return

    # Initialize the database
    try:
        db = bdb.database(db_directory).use()
    except FileNotFoundError:
        print(f"The directory '{db_directory}' does not exist.")
        return
    except PermissionError:
        print(f"You do not have permission to access the directory '{db_directory}'.")
        return
    except Exception as e:
        print(f"Error initializing the database: {e}")
        return

    while True:
        # Choose a table to load
        table_name = input("Enter the name of the table you want to use (without the .pydb extension): ").strip()

        # Check if the table exists in the directory
        table_file = f"{table_name}.pydb"
        if table_file not in files:
            print(f"Table '{table_name}' not found. Please enter a valid table name from the list above.")
            continue

        try:
            # Attempt to load the table
            tb1 = db.load_table(table_name)
            print("Current table:")
            print(tb1)
            break  # Exit the loop if the table is successfully loaded
        except FileNotFoundError:
            print(f"The table '{table_name}' could not be found in the directory.")
        except PermissionError:
            print(f"You do not have permission to access the table file '{table_file}'.")
        except Exception as e:
            print(f"Error loading the table '{table_name}': {e}")

if __name__ == "__main__":
    use_table()
