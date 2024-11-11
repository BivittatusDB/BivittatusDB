import BivittatusDB as bdb
from DB_manage.funtions.common.list_dir_pydb import list_pydb
from DB_manage.funtions.common.saving import save_table
from DB_manage.funtions.common.user_interaction_common import get_db_choice
from bdb_aggregate import delay, pause_and_clean

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
        print(f"Initializing database: {db_name}")
        db = bdb.Database(db_name).init()
        print(f"Loading table: {table_name}")
        table = db(table_name)
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

def update_tb():
    try:
        # Get the user's choice (load existing DB or create a new one)
        db_choice = get_db_choice()

        if db_choice == "y":
            # Prompt the user to enter the database directory
            db_directory = get_input("Enter the database directory: ")
            if db_directory == 'exit':
                print("Operation canceled.")
                return

            # Use list_pydb to select the table
            print("Listing tables in the database...")
            db_directory, tables = list_pydb(db_directory)
            
            if not tables:
                print("Operation canceled or error occurred during listing.")
                return  # Exit if the user cancels or an error occurs

            # Prompt the user to select a table
            print("Available tables:", ", ".join(tables))
            table_name = get_input("Enter the table name you want to load: ", valid_options=tables)
            if table_name == 'exit':
                print("Operation canceled.")
                return

            # Initialize and update the selected table
            print(f"Selected database: {db_directory}, table: {table_name}")
            table = initialize_table(db_directory, table_name)
            if table is None:
                print("Error: Table could not be initialized.")
                return

            update_table(table)
            save_table(table)
        else:
            print("Invalid choice. Exiting.")
            return
    except Exception as e:
        print(f"General error: {e}")
        delay(2)

if __name__ == "__main__":
    update_tb()
