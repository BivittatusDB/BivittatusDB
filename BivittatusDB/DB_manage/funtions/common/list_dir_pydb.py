from bdb_aggregate import delay, pause_and_clean, show
import BivittatusDB as bdb

def list_pydb():
    """
    Prompts the user to enter the database folder name and table name, and initializes the database.
    """
    while True:
        db_directory = input("Enter the name of the database folder (or 'n' to cancel): ").strip()

        if db_directory.lower() == 'n':
            print("Operation canceled.")
            delay(0.8)
            return None, None

        try:
            tables = show(db_directory)
            if not tables:
                print(f"No tables found in directory '{db_directory}'.")
                return None, None
            break  # Exit loop if successful
        except Exception as e:
            print(f"Error retrieving tables from directory '{db_directory}': {e}")
            delay(1)
            continue  # Retry instead of returning None immediately

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
                return db_directory, table_name
            except Exception as e:
                print(f"Error loading the table '{table_name}': {e}")
                return None, None
