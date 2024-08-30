import os
import BivittatusDB as bdb
from bdb_aggregate import pause_and_clean

def get_valid_input(tb, prompt, valid_options=None, convert_func=None):
    while True:
        print(tb)  # Print the table for context

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

def update_tb():
    try:
        db_folder = input("Enter the name of the database folder: ")
        print(f"Database folder: {db_folder}")  # Debugging line
        
        if os.path.isdir(db_folder):
            update_db = bdb.database(db_folder).init()
            table_name = input("Enter the name of the table you want to load: ").strip()
            print(f"Table name: {table_name}")  # Debugging line
            tb = update_db.load_table(table_name)
            print(f"Loaded table: {tb}")  # Debugging line
        else:
            print(f"Error: The database directory '{db_folder}' does not exist.")
            return

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return

    while True:
        id_to_update = get_valid_input(tb, "Enter the id of the row you want to update or type 'exit' to stop: ", convert_func=int)
        print(f"ID to update: {id_to_update}")  # Debugging line
        
        if id_to_update == 'exit':
            print("Exiting data entry.")
            break

        new_name = get_valid_input(tb, "Enter the new name: ")
        print(f"New name: {new_name}")  # Debugging line
        
        if new_name == 'exit':
            print("Exiting data entry.")
            break

        tb["name"] = (new_name, tb["id"] == id_to_update)
        pause_and_clean(0.8)
        print("Updated table:")
        print(tb)

        while True:
            answer = input("Do you want to save this table? (y/n): ").strip().lower()
            if answer == "y":
                bdb.save(tb)  # Save the table using bdb.save function
                print("Table saved successfully.")
                break
            elif answer == "n":
                print("You chose not to save this table.")
                break
            else:
                print("Choose a correct option (y/n).")
