import BivittatusDB as bdb
from bdb_aggregate import pause_and_clean

def add_names_to_db():
    def get_input(prompt, valid_options=None):
        while True:
            choice = input(prompt).strip().lower()
            if valid_options and choice not in valid_options:
                print("Invalid choice. Try again.")
            else:
                return choice

    db_choice = get_input("Do you want to load an existing database (y/n): ", ["y", "n"])
    db_name = input("Enter the name of the database folder: ").strip()
    table_name = input("Enter the name of the table you want to load or create: ").strip()

    try:
        test_db = bdb.database(db_name).init()
        tb1 = test_db.load_table(table_name) if db_choice == "y" else test_db.New_table(
            table_name, ("id", "name"), (int(), str()), "id"
        )
        print(f"Table '{table_name}' successfully {'loaded' if db_choice == 'y' else 'created'}.")
    except Exception as e:
        print(f"Error loading or creating table: {e}")
        return

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

    print("The result of the table:")
    print(tb1)

    answer = get_input("Do you want to save this table? (y/n): ", ["y", "n"])
    if answer == "y":
        try:
            bdb.save(tb1)
            print("Table saved successfully.")
        except Exception as e:
            print(f"Error saving table: {e}")
    else:
        print("You chose not to save this table.")

if __name__ == "__main__":
    add_names_to_db()
