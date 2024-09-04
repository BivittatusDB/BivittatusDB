import BivittatusDB as bdb
from bdb_aggregate import pause_and_clean, show

def use_table():
    db_directory = input("Enter the name of the database directory: ")
    
    # Get the list of tables using the show function
    try:
        tables = show(db_directory)
        print(f"Tables found: {tables}")
    except Exception as e:
        print(f"Error retrieving tables: {e}")
        return

    try:
        db = bdb.database(db_directory).use()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing the database: {e}")
        return

    while True:
        # Show available tables
        print("Available tables:", ", ".join(tables))

        # Request the name of the table
        table_name = input("Enter the name of the table you want to use (without .pydb extension): ")

        # Check if the table exists
        if table_name not in tables:
            print(f"Table '{table_name}' not found. Please enter a valid table name from the list above.")
        else:
            try:
                # Load the selected table
                tb1 = db.load_table(table_name)
                pause_and_clean(0)
                print("The current table:")
                print(tb1)
                
                # Confirm exit
                if confirm_exit(tb1):
                    return True

                break  # Exit the loop if the table is loaded successfully
            except Exception as e:
                print(f"Error loading the table '{table_name}': {e}")

def confirm_exit(tb1):
    while True:
        exit_choice = input("Do you want to exit? (y): ")
        if exit_choice.lower() == 'y':
            pause_and_clean(0)
            return True
        else:
            pause_and_clean(0)
            print("To exit, please enter 'y'")
            print("The current table:")
            print(tb1)

if __name__ == "__main__":
    use_table()
