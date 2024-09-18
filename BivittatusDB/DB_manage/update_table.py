import BivittatusDB as bdb
from DB_manage.metadata import list_pydb
from DB_manage.funtions.common.saving import save_table
from bdb_aggregate import pause_and_clean

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
