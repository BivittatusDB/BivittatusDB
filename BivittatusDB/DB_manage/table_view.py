import BivittatusDB as bdb
from bdb_aggregate import pause_and_clean, show, delay
from DB_manage.funtions.common.user_interaction_common import get_db_choice

def use_table():
    db_choice = get_db_choice()

    if db_choice == "y":
        db_directory = input("Enter the name of the database directory: ").strip()
        
        try:
            tables = show(db_directory)
            db = bdb.database(db_directory).use()
            print("Database initialized successfully.")
        except Exception as e:
            print(f"Error: {e}")
            delay(1.5)
            return

        while True:
            print("Available tables:", ", ".join(tables))
            table_name = input("Enter the name of the table you want to use (without .pydb extension): ").strip()

            if table_name in tables:
                try:
                    tb1 = db.load_table(table_name)
                    pause_and_clean(0)
                    print("The current table:")
                    print(tb1)
                    
                    if confirm_exit(tb1):
                        return
                except Exception as e:
                    print(f"Error loading the table '{table_name}': {e}")
            else:
                print(f"Table '{table_name}' not found. Please enter a valid table name from the list above.")
    else:
        print("Invalid choice. Exiting.")

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

if __name__ == "__main__":
    use_table()
