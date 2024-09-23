from DB_manage.funtions.removing.rm_rows import remove_rows_from_table
from DB_manage.funtions.common.db_utils import initialize_database, load_existing_table
from DB_manage.funtions.common.list_dir_pydb import list_pydb
from DB_manage.funtions.common.user_interaction_common import get_db_choice
from DB_manage.funtions.common.saving import save_table

def remove_rows():
    """
    Handles the process of selecting a database and table, removing rows, and saving the table.
    """
    db_choice = get_db_choice()

    tb1 = None
    if db_choice == "y":
        try:
            db_directory = input("Enter the database directory: ").strip()
            if not db_directory:
                print("Error: No directory provided.")
                return

            db_directory, tables = list_pydb(db_directory)
            if not tables:
                print("Error: No valid tables found in the directory.")
                return

            print("Available tables:", tables)
            table_name = input("Enter the table name you want to load: ").strip()
            if table_name not in tables:
                print(f"Error: Table '{table_name}' not found in the directory.")
                return

            tb1 = load_existing_table(db_directory, table_name)
            if tb1 is None:
                print("Error: Table could not be loaded.")
                return
        except Exception as e:
            print(f"Error loading existing table: {e}")
            return
    else:
        try:
            # Assuming that get_db_choice() returns db_name and table_name
            db_name, table_name = get_db_choice()
            tb1 = initialize_database(db_name, table_name)
            if tb1 is None:
                print("Error: Table could not be initialized.")
                return
        except Exception as e:
            print(f"Error initializing database: {e}")
            return

    try:
        remove_rows_from_table(tb1)
    except Exception as e:
        print(f"Error during row removal: {e}")

    print("Final table result:")
    print(tb1)

    try:
        save_table(tb1)
    except Exception as e:
        print(f"Error saving table: {e}")

if __name__ == "__main__":
    remove_rows()
