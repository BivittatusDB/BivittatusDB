from DB_manage.funtions.adding.user_interaction import get_db_choice, get_db_and_table_names
from DB_manage.funtions.adding.table_utils import add_names_to_table
from DB_manage.funtions.adding.db_utils import load_existing_table, create_new_table
from DB_manage.funtions.common.saving import save_table

def add_names_to_db():
    """
    Manages the process of adding names to a database table.
    Prompts the user to choose between loading an existing database or creating a new one,
    and then adds names to the selected table.
    """
    try:
        # Get the user's choice (load existing DB or create a new one)
        db_choice = get_db_choice()

        if db_choice == "y":
            # Load existing DB and table
            db_name, table_name = get_db_and_table_names()
            if db_name is None or table_name is None:
                return
            tb1 = load_existing_table(db_name, table_name)
        elif db_choice == "n":
            # Create new DB and table
            db_name = input("Enter a name for your DB: ").strip()
            table_name = input("Enter a name for the new table: ").strip()
            tb1 = create_new_table(db_name, table_name)
        else:
            print("Invalid choice. Exiting.")
            return

        if tb1 is not None:
            # Add names to the table
            add_names_to_table(tb1)
            print("The result of the table:")
            print(tb1)
            # Save the table
            save_table(tb1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    add_names_to_db()
