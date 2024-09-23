from bdb_aggregate import pause_and_clean, show, delay
import BivittatusDB as bdb

#Needs a fix (double n to cancel)
def get_db_choice():
    while True:
        choice = input("Do you want to load an existing database (y/n): ").strip().lower()
        if choice == 'n':
            print("Operation canceled.")
            return None  # Return None to indicate cancellation
        elif choice == 'y':
            return 'y'  # Return 'y' to indicate loading an existing database
        print("Invalid input. Please enter 'y' or 'n'.")

#Implemented on adding.py (Needs changes)
def get_db_and_table_names():
    """
    Prompts the user to enter the database folder name and table name, and initializes the database.
    Allows the user to cancel the operation.
    
    Returns:
        tuple: (db_directory, table_name) if successful, (None, None) otherwise.
    """
    db_directory = input("Enter the name of the database folder (or 'n' to cancel): ").strip()
    
    if db_directory.lower() == 'n':
        print("Operation canceled.")
        delay(0.8)
        return None, None

    try:
        tables = show(db_directory)
    except Exception as e:
        print(f"Error retrieving tables: {e}")
        delay(1)
        return None, None

    try:
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
                db.load_table(table_name)
                return db_directory, table_name
            except Exception as e:
                print(f"Error loading the table '{table_name}': {e}")
