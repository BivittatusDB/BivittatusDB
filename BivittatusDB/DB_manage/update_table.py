import os
import BivittatusDB as bdb
from bdb_aggregate import pause_and_clean

# Please add show() to remove listing on this current module

def get_input(prompt, valid_options=None, convert_func=None):
    while True:
        user_input = input(prompt).strip()
        if user_input.lower() == 'exit':
            return 'exit'
        if valid_options and user_input not in valid_options:
            print(f"Invalid input. Please enter one of the following: {', '.join(valid_options)}")
            continue
        if convert_func:
            try:
                user_input = convert_func(user_input)
            except ValueError:
                print(f"Invalid input. Please enter a valid {convert_func.__name__}.")
                continue
        return user_input

def list_database_files(db_directory, extension=".pydb"):
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
    try:
        update_db = bdb.database(db_name).init()
        tb = update_db.load_table(table_name)
        print(f"Table '{table_name}' successfully loaded.")
        return tb
    except Exception as e:
        print(f"Error loading table: {e}")
        return None

def update_table(tb):
    while True:
        pause_and_clean(0)
        print(tb)  # Ensure the table is printed here
        id_to_update = get_input("Enter the id of the row you want to update or type 'exit' to stop: ", convert_func=int)
        if id_to_update == 'exit':
            print("Exiting data entry.")
            break

        new_name = get_input("Enter the new name: ")
        if new_name == 'exit':
            print("Exiting data entry.")
            break

        try:
            tb["name"] = (new_name, tb["id"] == id_to_update)
            pause_and_clean(0)
            print("Updated table:")
            print(tb)
            pause_and_clean(1.2)
        except Exception as e:
            print(f"Error updating table: {e}")
            pause_and_clean(0.8)

def save_table(tb):
    answer = get_input("Do you want to save the table? (y/n): ", ["y", "n"])
    if answer == "y":
        try:
            bdb.save(tb)
            print("Table saved successfully.")
            pause_and_clean(0.8)
        except Exception as e:
            print(f"Error saving the table: {e}")
            pause_and_clean(0.8)
    else:
        print("You chose not to save this table.")

def update_tb():
    current_db = input("Enter the database you are going to use: ").strip()

    if not os.path.isdir(current_db):
        print(f"Error: The database directory '{current_db}' does not exist.")
        pause_and_clean(1)
        return

    # List .pydb files in the database directory
    files = list_database_files(current_db)
    if not files:
        print("There are no files with the .pydb extension in the database directory.")
        pause_and_clean(1)
        return

    while True:
        print("Files with the .pydb extension in the database directory:")
        for file in files:
            print(file)
        
        current_tb = input("Enter the table you are going to use: ").strip()
        if f"{current_tb}.pydb" in files:
            break
        else:
            print(f"Table '{current_tb}' not found. Please enter a valid table name from the list above.")
            pause_and_clean(1)

    tb = initialize_table(current_db, current_tb)
    if tb is None:
        return

    update_table(tb)
    save_table(tb)

def show(db_directory, extension=".pydb"):
    if not os.path.isdir(db_directory):
        print(f"Directory '{db_directory}' does not exist.")
        return []

    try:
        files = [f for f in os.listdir(db_directory) if f.endswith(extension)]
        if files:
            print("Files with the .pydb extension:")
            for file in files:
                print(file)
        else:
            print("No .pydb files found.")
        return files
    except PermissionError:
        print(f"You do not have permission to access the directory '{db_directory}'.")
        return []
    except Exception as e:
        print(f"An error occurred while listing files: {e}")
        return []

if __name__ == "__main__":
    update_tb()
