import BivittatusDB as bdb
from bdb_aggregate import pause_and_clean
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

def add_names_to_db():
    try:
        # Prompt the user for the choice of database
        db_choice = input("Do you want to load an existing database (y) or create a new one (n)? ").strip().lower()
        db_directory = input("Enter the name of the database directory: ").strip()

        if db_choice == "y":
            # Print and list existing database files
            files = print_pydb_files(db_directory)
            if not files:
                print("No files found to load. Exiting.")
                return

            table_name = input("Enter the name of the table to load (without the .pydb extension): ").strip()
            if f"{table_name}.pydb" not in files:
                print(f"Table '{table_name}' not found in the directory.")
                return

            try:
                test_db = bdb.database(db_directory).init()  # Initialize existing database
                tb1 = test_db.load_table(table_name)  # Load the specified table
                print(f"Table '{table_name}' successfully loaded.")
                print(tb1)
            except Exception as e:
                print(f"Error loading table: {e}")
                return

        elif db_choice == "n":
            # For creating a new database
            db_name = input("Enter a name for your new database: ").strip()
            table_name = input("Enter a name for the new table: ").strip()

            try:
                test_db = bdb.database(db_name).init()  # Initialize new database
                tb1 = test_db.New_table(
                    table_name,  # Table name
                    ("id", "name"),  # Column names
                    (int, str),  # Column data types
                    "id"  # Primary key column
                )
                print("New table created.")
            except Exception as e:
                print(f"Error creating table: {e}")
                return

        else:
            print("Invalid choice. Exiting.")
            return

        # Determine the next ID for new entries
        try:
            if len(tb1) > 0:
                next_id = max(row[0] for row in tb1) + 1
            else:
                next_id = 1
        except Exception as e:
            print(f"Error determining next ID: {e}")
            return

        # Add names to the table
        while True:
            name = input("Enter a name to add to the table (or 'exit' to end): ").strip()
            if name.lower() == 'exit':
                break
            try:
                tb1 + (next_id, name)  # Add new row to the table
                next_id += 1  # Increment ID for the next entry
                print(f"Succesfull adding name to table: {name}")
            except Exception as e:
                print(f"Error adding name to table: {e}")

        # Display the result
        print("The result of the table:")
        print(tb1)

        # Ask if the user wants to save the changes
        while True:
            answer = input("Do you want to save this table? (y/n): ").strip().lower()
            if answer == "y":
                try:
                    bdb.save(tb1)  # Save the table
                    print("Table saved successfully.")
                    pause_and_clean(0.4)
                except Exception as e:
                    print(f"Error saving table: {e}")
                finally:
                    return
            elif answer == "n":
                print("You chose not to save this table.")
                return
            else:
                print("Choose a correct option (y/n).")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    add_names_to_db()
