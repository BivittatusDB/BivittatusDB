import BivittatusDB as bdb
from DB_manage.list_pydb import list_db_files

def print_pydb_files(db_directory):
    files = list_db_files(db_directory)
    if not files:
        print("There are no files with the .pydb extension in the database directory.")
    else:
        print("Files with the .pydb extension in the database directory:")
        for file in files:
            print(file)
    return files

def remove_rows():
    try:
        # Ask if you want to load an existing database
        db_choice = input("Do you want to load an existing database (y/n): ").strip().lower()

        if db_choice == "y":
            db_name = input("Enter the name of the database directory: ").strip()
            
            # List existing database files
            files = print_pydb_files(db_name)
            if not files:
                print("No files found to load. Exiting.")
                return

            table_name = input("Enter the name of the table you want to load (without the .pydb extension): ").strip()
            table_file = f"{table_name}.pydb"

            if table_file not in files:
                print(f"Table '{table_name}' not found in the directory.")
                return

            try:
                # Load the database and the table
                test_db = bdb.database(db_name).init()
                tb1 = test_db.load_table(table_name)
                print(f"Table '{table_name}' successfully loaded.")
                print(tb1)
            except Exception as e:
                print(f"Error loading table: {e}")
                return

        elif db_choice == "n":
            print("The option to create a new database or table is not implemented.")
            return

        else:
            print("Invalid option. Exiting.")
            return

        while True:
            # Request value to delete in the fixed column
            value_to_delete = input("Enter the value you wish to delete in the 'name' column (or 'exit' to exit): ").strip()
            if value_to_delete.lower() == 'exit':
                break

            # Attempt to delete rows corresponding to the value entered
            try:
                tb1["name"] - value_to_delete
                print(f"Rows with value '{value_to_delete}' in column 'name' successfully deleted.")
            except AttributeError:
                print(f"The table object does not have the 'remove_rows' method.")
            except Exception as e:
                print(f"Error deleting rows: {e}")

        print("Final table result:")
        print(tb1)

        while True:
            answer = input("Do you want to save this table (y/n)? ").strip().lower()
            if answer == "y":
                try:
                    bdb.save(tb1)
                    print("Table successfully saved.")
                except Exception as e:
                    print(f"Error saving the table: {e}")
                break
            elif answer == "n":
                print("You have chosen not to save the table.")
                break
            else:
                print("Please choose a correct option (y/n).")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    remove_rows()
