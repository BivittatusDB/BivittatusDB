from bdb_aggregate import pause_and_clean, show, delay
import BivittatusDB as bdb

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
    """
    db_directory = input("Enter the name of the database folder: ").strip()

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
                tb1 = db.load_table(table_name)
                #pause_and_clean(2)
                return db_directory, table_name
            except Exception as e:
                print(f"Error loading the table '{table_name}': {e}")
