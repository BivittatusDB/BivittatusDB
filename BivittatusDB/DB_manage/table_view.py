import BivittatusDB as bdb
from bdb_aggregate import pause_and_clean, show, delay
from DB_manage.funtions.common.user_interaction_common import get_db_choice

def use_table():
    # Get the user's choice (load existing DB or create a new one)
    db_choice = get_db_choice()

    if db_choice == "y":
        db_directory = input("Enter the name of the database directory: ")
        
        # Get the list of tables using the show function
        try:
            tables = show(db_directory)
        except Exception as e:
            print(f"Error retrieving tables: {e}")
            delay(1.5)
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
    else:
        print("Invalid choice. Exiting.")
        return

def confirm_exit(tb1):
    while True:
        exit_choice = input("Do you want to exit? (y): ")
        if exit_choice.strip() == 'y':
            pause_and_clean(0)
            return True
        else:
            pause_and_clean(0)
            print("To exit, please enter 'y'")
            print("The current table:")
            print(tb1)

if __name__ == "__main__":
    use_table()
