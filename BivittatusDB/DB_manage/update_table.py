import BivittatusDB as bdb
from DB_manage.funtions.common.saving import save_table
from bdb_aggregate import pause_and_clean, delay, show

def get_input(prompt, valid_options=None, convert_func=None):
    while True:
        user_input = input(prompt).strip()
        if user_input.lower() == 'exit':
            return 'exit'
        if valid_options and user_input not in valid_options:
            print(f"Invalid input. Please enter one of the following: {', '.join(valid_options)}")
        else:
            if convert_func:
                try:
                    user_input = convert_func(user_input)
                except ValueError:
                    print(f"Invalid input. Please enter a valid {convert_func.__name__}.")
                    continue
            return user_input

def initialize_table(db_name, table_name):
    try:
        db = bdb.database(db_name).init()
        table = db.load_table(table_name)
        print(f"Table '{table_name}' successfully loaded.")
        return table
    except Exception as e:
        print(f"Error loading table: {e}")
        return None

def update_table(table):
    while True:
        pause_and_clean(0)
        print(table)
        id_to_update = get_input("Enter the id of the row you want to update or type 'exit' to stop: ", convert_func=int)
        if id_to_update == 'exit':
            print("Exiting data entry.")
            break

        new_name = get_input("Enter the new name: ")
        if new_name == 'exit':
            print("Exiting data entry.")
            break

        try:
            table["name"] = (new_name, table["id"] == id_to_update)
            pause_and_clean(0)
            print("Updated table:")
            print(table)
            pause_and_clean(1.2)
        except Exception as e:
            print(f"Error updating table: {e}")
            pause_and_clean(0.8)

def list_pydb():
    """
    Prompts the user to enter the database folder name and table name, and initializes the database.
    
    Returns:
        tuple: (db_directory, table_name) if successful, (None, None) if canceled or if an error occurs.
    """
    while True:
        db_directory = input("Enter the name of the database folder (or 'n' to cancel): ").strip()

        if db_directory.lower() == 'n':
            print("Operation canceled.")
            delay(0.8)
            return None, None

        try:
            # Attempt to display the tables in the directory
            tables = show(db_directory)
            if not tables:
                print(f"No tables found in directory '{db_directory}'.")
                return None, None
            break  # Exit loop if successful
        except Exception as e:
            print(f"Error retrieving tables from directory '{db_directory}': {e}")
            delay(1)
            continue  # Retry instead of returning None immediately

    try:
        # Initialize the database
        db = bdb.database(db_directory).use()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing the database: {e}")
        return None, None

    while True:
        print("Available tables:", ", ".join(tables))
        table_name = input("Enter the name of the table you want to use (without .pydb extension): ").strip()

        if table_name not in tables:
            pause_and_clean(0)
            print(f"Table '{table_name}' not found. Please enter a valid table name from the list above.")
        else:
            try:
                # Load the selected table
                tb1 = db.load_table(table_name)
                print(f"Table '{table_name}' loaded successfully.")
                return db_directory, table_name
            except Exception as e:
                print(f"Error loading the table '{table_name}': {e}")
                return None, None

def update_tb():
    # Use list_pydb to select the database and table
    db_directory, table_name = list_pydb()
    
    if db_directory is None or table_name is None:
        return  # Exit if the user cancels or an error occurs

    # Initialize and update the selected table
    table = initialize_table(db_directory, table_name)
    if table is None:
        return

    update_table(table)
    save_table(table)

if __name__ == "__main__":
    update_tb()
