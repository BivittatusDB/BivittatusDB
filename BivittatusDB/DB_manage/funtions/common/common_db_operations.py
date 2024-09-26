from DB_manage.funtions.common.list_dir_pydb import list_pydb
from DB_manage.funtions.common.db_utils import load_existing_table
from DB_manage.funtions.common.user_interaction_common import get_db_choice

def get_table_from_db():
    db_choice = get_db_choice()
    tb1 = None

    if db_choice == "y":
        db_directory = input("Enter the database directory: ").strip()
        if not db_directory:
            print("Error: No directory provided.")
            return None

        db_directory, tables = list_pydb(db_directory)
        if not tables:
            print("Error: No valid tables found in the directory.")
            return None

        print("Available tables:", ", ".join(tables))
        table_name = input("Enter the table name you want to load: ").strip()
        if table_name not in tables:
            print(f"Error: Table '{table_name}' not found in the directory.")
            return None

        tb1 = load_existing_table(db_directory, table_name)
        if tb1 is None:
            print("Error: Table could not be loaded.")
            return None

    elif db_choice == "n":
        db_name = input("Enter a name for your DB: ").strip()
        table_name = input("Enter a name for the new table: ").strip()
        # here you should define or import `create_new_table` if needed
        # tb1 = create_new_table(db_name, table_name)
        # For demonstration purposes, let's assume that `create_new_table` is not defined.
        print("The function 'create_new_table' is not defined. Please define it or remove this part.")
        return None

    else:
        print("Invalid choice. Exiting.")
        return None

    return tb1
