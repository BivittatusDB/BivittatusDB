from DB_manage.update_table import update_tb
from DB_manage.removing_rows import remove_rows
from DB_manage.adding_rows import add_names_to_db
from DB_manage.table_view import use_table
from bdb_aggregate import pause_and_clean

def display_menu():
    """
    Displays the main menu options to the user.
    """
    menu_options = [
        "Option 1: Use table",
        "Option 2: Insert values in table",
        "Option 3: Delete values in the table",
        "Option 4: Update values in the table",
        "Option 5: Print metadata",
        "Option 6: Exit"
    ]
    print("\nWhat do you want to do?")
    for option in menu_options:
        print(option)

def execute_option(option):
    try:
        if option == "1":
            use_table()
            pause_and_clean(1.2)
        elif option == "2":
            pause_and_clean(0.2)
            add_names_to_db()
        elif option == "3":
            remove_rows()
            pause_and_clean(0.8)
        elif option == "4":
            update_tb()
        elif option == "5":
            print("This option is not working right now.")
            pause_and_clean(1)
        elif option == "6":
            print("Exiting....")
            pause_and_clean(0.4)
            return False
        else:
            print("Incorrect option. Please choose a valid option.")
            pause_and_clean(0.8)
        return True
    except Exception as e:
        print(f"Exception: {e}")
        pause_and_clean(1)

def main_menu():
    """
    Displays the main menu and handles user input until the user chooses to exit.
    """
    try:
        while True:
            display_menu()
            option = input("Please enter an option: ").strip()
            if not execute_option(option):
                break
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt detected. Exiting...")
        pause_and_clean(0.8)

if __name__ == "__main__":
    main_menu()
