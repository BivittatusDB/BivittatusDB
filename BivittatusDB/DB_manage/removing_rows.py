from DB_manage.funtions.removing.rm_rows import remove_rows_from_table
from DB_manage.funtions.common.db_utils import initialize_database, load_existing_table
from DB_manage.funtions.common.list_dir_pydb import list_pydb
from DB_manage.funtions.common.user_interaction_common import get_db_choice
from DB_manage.funtions.common.saving import save_table

def remove_rows():
    db_choice = get_db_choice()
    tb1 = None

    try:
        if db_choice == "y":
            db_directory = input("Enter the database directory: ").strip()
            if not db_directory:
                print("Error: No directory provided.")
                return

            db_directory, tables = list_pydb(db_directory)
            if not tables:
                print("Error: No valid tables found in the directory.")
                return

            print("Available tables:", ", ".join(tables))
            table_name = input("Enter the table name you want to load: ").strip()
            if table_name not in tables:
                print(f"Error: Table '{table_name}' not found in the directory.")
                return

            tb1 = load_existing_table(db_directory, table_name)
            if tb1 is None:
                print("Error: Table could not be loaded.")
                return
        elif db_choice is None:
            print("Operation canceled.")
            return
        else:
            db_name, table_name = get_db_choice()
            tb1 = initialize_database(db_name, table_name)
            if tb1 is None:
                print("Error: Table could not be initialized.")
                return

        remove_rows_from_table(tb1)
        print("Final table result:")
        print(tb1)
        save_table(tb1)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    remove_rows()
