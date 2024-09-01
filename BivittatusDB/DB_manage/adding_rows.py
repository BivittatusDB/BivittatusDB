import BivittatusDB as bdb
from bdb_aggregate import pause_and_clean

def get_db_choice():
    return input("Do you want to load an existing database (y/n): ").strip().lower()

def get_db_and_table_names():
    db_name = input("Enter the name of the database folder: ").strip()
    table_name = input("Enter the name of the table you want to load: ").strip()
    return db_name, table_name

def load_existing_table(db_name, table_name):
    try:
        test_db = bdb.database(db_name).init()
        tb1 = test_db.load_table(table_name)
        print(f"Table '{table_name}' successfully loaded.")
        pause_and_clean(0.8)
        return tb1
    except Exception as e:
        print(f"Error loading table: {e}")
        return None

def create_new_table(db_name, table_name):
    try:
        test_db = bdb.database(db_name).init()
        tb1 = test_db.New_table(
            table_name,
            ("id", "name"),
            (int(), str()),
            "id"
        )
        print("New table created.")
        return tb1
    except Exception as e:
        print(f"Error creating table: {e}")
        return None

def get_next_id(tb1):
    try:
        if len(tb1) > 0:
            return max(row[0] for row in tb1) + 1
        else:
            return 1
    except Exception as e:
        print(f"Error determining next ID: {e}")
        return None

def add_names_to_table(tb1):
    id = get_next_id(tb1)
    if id is None:
        return

    while True:
        pause_and_clean(0)
        print(tb1)
        name = input("Enter a name to add to the table (or 'exit' to end): ").strip()
        if name.lower() == 'exit':
            break
        try:
            tb1 + (id, name)
            id += 1
        except Exception as e:
            print(f"Error adding name to table: {e}")

def save_table(tb1):
    answer = input("Do you want to save this table? (y/n): ").strip().lower()
    if answer == "y":
        try:
            bdb.save(tb1)
            print("Table saved successfully.")
            pause_and_clean(0.8)
        except Exception as e:
            print(f"Error saving table: {e}")
    elif answer == "n":
        print("You chose not to save this table.")
    else:
        print("Choose a correct option (y/n).")

def add_names_to_db():
    try:
        db_choice = get_db_choice()
        if db_choice == "y":
            db_name, table_name = get_db_and_table_names()
            tb1 = load_existing_table(db_name, table_name)
        elif db_choice == "n":
            db_name = input("Enter a name for your DB: ").strip()
            table_name = input("Enter a name for the new table: ").strip()
            tb1 = create_new_table(db_name, table_name)
        else:
            print("Invalid choice. Exiting.")
            return

        if tb1 is not None:
            add_names_to_table(tb1)
            print("The result of the table:")
            print(tb1)
            save_table(tb1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    add_names_to_db()
