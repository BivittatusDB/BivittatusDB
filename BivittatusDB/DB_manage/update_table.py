import os
import BivittatusDB as bdb
from bdb_aggregate import pause_and_clean

# Initialize the database
def update_tb():
    try:
        pause_and_clean(0)  # Assuming this function exists to clear the screen
        current_db = input("Enter the database you are going to use: ")

        # Check if the database directory exists
        if os.path.isdir(current_db):
            update_db = bdb.database(current_db).init()

            current_tb = input("Enter the table you are going to use: ")
            tb = update_db.load_table(current_tb)
        else:
            print(f"Error: The database directory '{current_db}' does not exist.")
            return

        # Function to get valid input from the user
        def get_valid_input(prompt, valid_options=None, convert_func=None):
            while True:
                pause_and_clean(0)
                print(tb)

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

        # Loop to allow user to update data or exit
        while True:
            id_to_update = get_valid_input("Enter the id of the row you want to update or type 'exit' to stop: ", convert_func=int)

            if id_to_update == 'exit':
                print("Exiting data entry.")
                break

            new_name = get_valid_input("Enter the new name: ")

            if new_name == 'exit':
                print("Exiting data entry.")
                break

            # Update the table based on user input
            tb["name"] = (new_name, tb["id"] == id_to_update)
            pause_and_clean(0)
            print("Updated table:")
            print(tb)

            
            answer = input("Do you want to save the table? (y/n): ").strip().lower()
            if answer == "y":
                bdb.save(tb)  # Save the table using bdb.save function
                print("Table saved successfully.")
                break  # Exit the loop after saving the table
            elif answer == "n":
                print("You chose not to save this table.")
                break  # Exit the loop after deciding not to save the table
            else:
                print("Choose a correct option (y/n).")

    except Exception as e:
        print(f"An error occurred: {str(e)}")