import BivittatusDB as bdb
from DB_manage.file_operations import get_files_with_extension

def show_files_with_extension(db_directory, extension=".pydb"):
    """
    Lists files in the specified directory that match the given extension.

    :param db_directory: Path to the database directory.
    :param extension: File extension to filter by (default is '.pydb').
    :return: List of file names with the specified extension.
    """
    files = get_files_with_extension(db_directory, extension)

    if not files:
        print(f"There are no files with the '{extension}' extension in the database directory.")
    else:
        print(f"Files with the '{extension}' extension in the database directory:")
        for file in files:
            print(file)
    return files

def use_table():
    """
    Allows the user to select a table from the database directory and load it.
    """
    # Prompt the user for the name of the database directory
    db_directory = input("Enter the name of the database directory: ").strip()

    # Show available files with the .pydb extension in the directory
    files = show_files_with_extension(db_directory)
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
        # Prompt user to choose a table
        table_name = input("Enter the name of the table you want to use (without the .pydb extension): ").strip()

        # Form the complete file name to check
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

