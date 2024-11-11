import os
import BivittatusDB as bdb
from bdb_aggregate import pause_and_clean, show, delay
from DB_manage.funtions.common.user_interaction_common import get_db_choice

def initialize_database(db_directory):
    # Check if the directory exists
    if not os.path.exists(db_directory):
        print(f"Error: The directory '{db_directory}' does not exist.")
        return None, None

    try:
        tables = show(db_directory)
        db = bdb.Database(db_directory).use()
        print("Database initialized successfully.")
        return db, tables
    except Exception as e:
        print(f"Error: {e}")
        delay(1.5)
        return None, None

def load_table(db, tables):
    while True:
        print("Available tables:", ", ".join(tables))
        table_name = input("Enter the name of the table you want to use (without .pydb extension): ").strip()

        if table_name in tables:
            try:
                tb1 = db.load_table(table_name)
                pause_and_clean(0)
                print("The current table:")
                print(tb1)
                return tb1
            except Exception as e:
                print(f"Error loading the table '{table_name}': {e}")
        else:
            print(f"The table '{table_name}' was not found. Please enter a valid name from the list above.")

def confirm_exit(tb1):
    while True:
        exit_choice = input("Do you want to exit? (y): ").strip().lower()
        if exit_choice == 'y':
            pause_and_clean(0)
            return True
        else:
            print("To exit, please enter 'y'")
            pause_and_clean(0.8)
            print("The current table:")
            print(tb1)

def use_table():
    db_choice = get_db_choice()

    if db_choice == "y":
        db_directory = input("Enter the name of the database directory: ").strip()
        db, tables = initialize_database(db_directory)
        if db and tables:
            tb1 = load_table(db, tables)
            if tb1:
                confirm_exit(tb1)
    else:
        print("Invalid option. Exiting.")

if __name__ == "__main__":
    use_table()
