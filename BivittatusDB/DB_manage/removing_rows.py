import os
import BivittatusDB as bdb
from bdb_aggregate import pause_and_clean, show

def get_input(prompt, valid_options=None):
    """
    Prompts the user for input and validates it against a list of valid options.
    
    Args:
        prompt (str): The prompt to display to the user.
        valid_options (list, optional): A list of valid options. Defaults to None.
    
    Returns:
        str: The user's input, stripped and converted to lowercase.
    """
    while True:
        choice = input(prompt).strip().lower()
        if valid_options and choice not in valid_options:
            print("Invalid choice. Try again.")
        else:
            return choice

def list_database_files(db_directory, extension=".pydb"):
    """
    Lists files with a specific extension in a given directory.
    
    Args:
        db_directory (str): The directory to search for files.
        extension (str, optional): The file extension to search for. Defaults to ".pydb".
    
    Returns:
        list: A list of filenames with the specified extension.
    """
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

def initialize_table(db_name, table_name):
    """
    Initializes a table from a database.
    
    Args:
        db_name (str): The name of the database.
        table_name (str): The name of the table to load.
    
    Returns:
        object: The loaded table, or None if an error occurred.
    """
    try:
        test_db = bdb.database(db_name).init()
        tb1 = test_db.load_table(table_name)
        print(f"Table '{table_name}' successfully loaded.")
        print(tb1)
        return tb1
    except Exception as e:
        print(f"Error loading table: {e}")
        return None

def remove_rows_from_table(tb1):
    """
    Removes rows from a table based on user input.
    
    Args:
        tb1 (object): The table from which to remove rows.
    """
    while True:
        pause_and_clean(0)
        print(tb1)
        value_to_delete = input("Enter the value you wish to delete in the 'name' column (or 'exit' to exit): ").strip()
        if value_to_delete.lower() == 'exit':
            pause_and_clean(0)
            break

        try:
            tb1["name"] - value_to_delete
            print(f"Rows with value '{value_to_delete}' in column 'name' successfully deleted.")
        except AttributeError:
            print("The table object does not have a remove_rows method.")
        except Exception as e:
            print(f"Error when deleting rows: {e}")

def save_table(tb1):
    """
    Prompts the user to save the table and saves it if the user chooses to.
    
    Args:
        tb1 (object): The table to save.
    """
    answer = get_input("Do you want to save this table (y/n)? ", ["y", "n"])
    if answer == "y":
        try:
            bdb.save(tb1)
            print("Table successfully saved.")
            pause_and_clean(0.8)
        except Exception as e:
            print(f"Error saving the table: {e}")
            pause_and_clean(0.8)
    else:
        print("You have chosen not to save the table.")
        pause_and_clean(1)

def remove_rows():
    """
    Manages the process of removing rows from a database table.
    Prompts the user to choose between loading an existing database or creating a new one,
    and then removes rows from the selected table.
    """
    print("Input 'n' to get back to the main menu")
    db_choice = get_input("Do you want to load an existing database (y/n): ", ["y", "n"])
    if db_choice == "y":
        db_name = input("Enter the name of the database directory: ").strip()
        
        # List .pydb files in the database directory
        files = list_database_files(db_name)
        if not files:
            print("There are no files with the .pydb extension in the database directory.")
            pause_and_clean(2)
            return

        while True:
            print("Files with the .pydb extension in the database directory:")
            for file in files:
                print(file)

            table_name = input("Enter the name of the table you want to load: ").strip()
            if f"{table_name}.pydb" in files:
                break
            else:
                print(f"Table '{table_name}' not found. Please enter a valid table name from the list above.")
                pause_and_clean(1)

        tb1 = initialize_table(db_name, table_name)
        if tb1 is None:
            return

        remove_rows_from_table(tb1)
        print("Final table result:")
        print(tb1)
        save_table(tb1)

if __name__ == "__main__":
    remove_rows()
