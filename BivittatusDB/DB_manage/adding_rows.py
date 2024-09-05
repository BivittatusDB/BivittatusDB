import os
import BivittatusDB as bdb
from bdb_aggregate import pause_and_clean, show, delay

def get_db_choice():
    while True:
        print("To create a new database input: 'n'")
        choice = input("Do you want to load an existing database (y/n): ").strip().lower()
        if choice in ['y', 'n']:
            return choice
        else:
            print("Invalid input. Please enter 'y' or 'n'.")


def get_db_and_table_names():
    """
    Prompts the user to enter the database folder name and table name, and initializes the database.

    Returns:
        tuple: (db_directory, table_name) if successful, (None, None) otherwise.
    """
    db_directory = input("Enter the name of the database folder: ").strip()
    
    # Retrieve the list of tables
    try:
        tables = show(db_directory)
    except Exception as e:
        print(f"Error retrieving tables: {e}")
        delay(1)
        return None, None

    # Initialize the database
    try:
        db = bdb.database(db_directory).use()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing the database: {e}")
        return None, None

    # Prompt user to enter the table name
    while True:
        print("Available tables:", ", ".join(tables))
        table_name = input("Enter the name of the table you want to use (without .pydb extension): ").strip()
        
        if table_name not in tables:
            pause_and_clean(0)
            print(f"Table '{table_name}' not found. Please enter a valid table name from the list above.")
        else:
            try:
                tb1 = db.load_table(table_name)
                pause_and_clean(2)
                return db_directory, table_name
            except Exception as e:
                print(f"Error loading the table '{table_name}': {e}")

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

def load_existing_table(db_name, table_name):
    try:
        test_db = bdb.database(db_name).init()
        tb1 = test_db.load_table(table_name)
        print(f"Table '{table_name}' successfully loaded.")
        delay(1.5)
        return tb1
    except Exception as e:
        print(f"Error loading table: {e}")
        return None

def create_new_table(db_name, table_name):
    try:
        test_db = bdb.database(db_name).init()
        tb1 = test_db.New_table(
            table_name,
            ("id", "name"),
            (int(), str()),
            "id"
        )
        print("New table created.")
        return tb1
    except Exception as e:
        print(f"Error creating table: {e}")
        return None

def get_next_id(tb1):
    try:
        if len(tb1) > 0:
            return max(row[0] for row in tb1) + 1
        else:
            return 1
    except Exception as e:
        print(f"Error determining next ID: {e}")
        return None

def add_names_to_table(tb1):
    id = get_next_id(tb1)
    if id is None:
        return

    while True:
        pause_and_clean(0)
        print("The current table:")
        print(tb1)
        name = input("Enter a name to add to the table (or 'exit' to end): ").strip()
        if name.lower() == 'exit':
            pause_and_clean(0)
            break
        try:
            tb1 + (id, name)
            id += 1
        except Exception as e:
            print(f"Error adding name to table: {e}")

def add_names_to_db():
    """
    Manages the process of adding names to a database table.
    Prompts the user to choose between loading an existing database or creating a new one,
    and then adds names to the selected table.
    """
    try:
        db_choice = get_db_choice()
        
        if db_choice == "y":
            db_name, table_name = get_db_and_table_names()
            if db_name is None or table_name is None:
                return
            tb1 = load_existing_table(db_name, table_name)
        elif db_choice == "n":
            db_name = input("Enter a name for your DB: ").strip()
            table_name = input("Enter a name for the new table: ").strip()
            tb1 = create_new_table(db_name, table_name)
        else:
            print("Invalid choice. Exiting.")
            return

        if tb1 is not None:
            add_names_to_table(tb1)
            print("The result of the table:")
            print(tb1)
            save_table(tb1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def save_table(tb1):
    answer = input("Do you want to save this table? (y/n): ").strip().lower()
    if answer == "y":
        try:
            bdb.save(tb1)
            print("Table saved successfully.")
            pause_and_clean(0.8)
        except Exception as e:
            print(f"Error saving table: {e}")
    elif answer == "n":
        print("You chose not to save this table.")
        delay(2)
    else:
        print("Choose a correct option (y/n).")

if __name__ == "__main__":
    add_names_to_db()
