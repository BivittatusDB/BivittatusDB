import BivittatusDB as bdb
from bdb_aggregate import pause_and_clean

def get_input(prompt, valid_options=None):
    while True:
        choice = input(prompt).strip().lower()
        if valid_options and choice not in valid_options:
            print("Invalid choice. Try again.")
        else:
            return choice

def initialize_table(db_name, table_name, db_choice):
    try:
        test_db = bdb.database(db_name).init()
        if db_choice == "y":
            tb1 = test_db.load_table(table_name)
            print(f"Table '{table_name}' successfully loaded.")
        else:
            tb1 = test_db.New_table(table_name, ("id", "name"), (int(), str()), "id")
            print("New table created.")
        return tb1
    except Exception as e:
        print(f"Error loading or creating table: {e}")
        return None

def add_names_to_table(tb1):
    id = max((row[0] for row in tb1), default=0) + 1
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
    answer = get_input("Do you want to save this table? (y/n): ", ["y", "n"])
    if answer == "y":
        try:
            bdb.save(tb1)
            print("Table saved successfully.")
            pause_and_clean(0.8)
        except Exception as e:
            print(f"Error saving table: {e}")
    else:
        print("You chose not to save this table.")

def add_names_to_db():
    db_choice = get_input("Do you want to load an existing database (y/n): ", ["y", "n"])
    db_name = input("Enter the name of the database folder: ").strip()
    table_name = input("Enter the name of the table you want to load or create: ").strip()

    tb1 = initialize_table(db_name, table_name, db_choice)
    if tb1 is None:
        return

    add_names_to_table(tb1)
    print("The result of the table:")
    print(tb1)
    save_table(tb1)

if __name__ == "__main__":
    add_names_to_db()
