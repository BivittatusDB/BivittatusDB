import BivittatusDB as bdb
from DB_manage.file_operations import get_files_with_extension

def print_pydb_files(db_directory):
    files = get_files_with_extension(db_directory)
    if files:
        print("Files with the .pydb extension in the database directory:")
        for file in files:
            print(file)
    else:
        print("There are no files with the .pydb extension in the database directory.")
    return files

def load_table(db_directory):
    files = print_pydb_files(db_directory)
    if not files:
        print("No files found to load. Exiting.")
        return None

    table_name = input("Enter the name of the table to load (without the .pydb extension): ").strip()
    table_file = f"{table_name}.pydb"

    if table_file in files:
        try:
            test_db = bdb.database(db_directory).init()
            tb1 = test_db.load_table(table_name)
            print(f"Table '{table_name}' successfully loaded.")
            print(tb1)
            return tb1
        except Exception as e:
            print(f"Error loading table: {e}")
            return None
    else:
        print(f"Table '{table_name}' not found in the directory.")
        return None

def delete_rows(tb1):
    while True:
        value_to_delete = input("Enter the value to delete in the 'name' column (or 'exit' to exit): ").strip()
        if value_to_delete.lower() == 'exit':
            break
        try:
            tb1["name"] - value_to_delete
            print(f"Rows with value '{value_to_delete}' in column 'name' successfully deleted.")
        except AttributeError:
            print("The table object does not support the 'remove_rows' method.")
        except Exception as e:
            print(f"Error deleting rows: {e}")

def save_table(tb1):
    while True:
        answer = input("Do you want to save this table (y/n)? ").strip().lower()
        if answer == "y":
            try:
                bdb.save(tb1)
                print("Table successfully saved.")
                break
            except Exception as e:
                print(f"Error saving the table: {e}")
        elif answer == "n":
            print("You have chosen not to save the table.")
            break
        else:
            print("Please choose a correct option (y/n).")

def remove_rows():
    try:
        db_choice = input("Do you want to load an existing database (y/n)? ").strip().lower()
        if db_choice == "y":
            db_name = input("Enter the name of the database directory: ").strip()
            tb1 = load_table(db_name)
            if tb1:
                delete_rows(tb1)
                save_table(tb1)
        elif db_choice == "n":
            print("The option to create a new database or table is not implemented.")
        else:
            print("Invalid option. Exiting.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    remove_rows()
