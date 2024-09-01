import BivittatusDB as bdb
from bdb_aggregate import pause_and_clean

def get_input(prompt, valid_options=None):
    while True:
        choice = input(prompt).strip().lower()
        if valid_options and choice not in valid_options:
            print("Invalid choice. Try again.")
        else:
            return choice

def initialize_table(db_name, table_name):
    try:
        test_db = bdb.database(db_name).init()
        tb1 = test_db.load_table(table_name)
        print(f"Table '{table_name}' successfully loaded.")
        print(tb1)
        return tb1
    except Exception as e:
        print(f"Error loading table: {e}")
        return None

def remove_rows_from_table(tb1):
    while True:
        pause_and_clean(0)
        print(tb1)
        value_to_delete = input("Enter the value you wish to delete in the 'name' column (or 'exit' to exit): ").strip()
        if value_to_delete.lower() == 'exit':
            break

        try:
            tb1["name"] - value_to_delete
            print(f"Rows with value '{value_to_delete}' in column 'name' successfully deleted.")
        except AttributeError:
            print("The table object does not have a remove_rows method.")
        except Exception as e:
            print(f"Error when deleting rows: {e}")

def save_table(tb1):
    answer = get_input("Do you want to save this table (y/n)? ", ["y", "n"])
    if answer == "y":
        try:
            bdb.save(tb1)
            print("Table successfully saved.")
            pause_and_clean(0.8)
        except Exception as e:
            print(f"Error saving the table: {e}")
            pause_and_clean(0.8)
    else:
        print("You have chosen not to save the table.")

def remove_rows():
    db_choice = get_input("Do you want to load an existing database (y/n): ", ["y", "n"])
    if db_choice == "y":
        db_name = input("Enter the name of the database directory: ").strip()
        table_name = input("Enter the name of the table you want to load: ").strip()

        tb1 = initialize_table(db_name, table_name)
        if tb1 is None:
            return

        remove_rows_from_table(tb1)
        print("Final table result:")
        print(tb1)
        save_table(tb1)

if __name__ == "__main__":
    remove_rows()