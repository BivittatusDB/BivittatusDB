import BivittatusDB as bdb
from bdb_aggregate import pause_and_clean

def add_names_to_db():
    try:
        db_choice = input("Do you want to load an existing database (y/n): ").strip().lower()
        if db_choice not in ["y", "n"]:
            print("Invalid choice. Exiting.")
            return

        db_name = input("Enter the name of the database folder: ").strip()
        table_name = input("Enter the name of the table you want to load or create: ").strip()

        try:
            test_db = bdb.database(db_name).init()
            if db_choice == "y":
                tb1 = test_db.load_table(table_name)
                print(f"Table '{table_name}' successfully loaded.")
            else:
                tb1 = test_db.New_table(
                    table_name,
                    ("id", "name"),
                    (int(), str()),
                    "id"
                )
                print("New table created.")
        except Exception as e:
            print(f"Error loading or creating table: {e}")
            return

        try:
            id = max(row[0] for row in tb1) + 1 if len(tb1) > 0 else 1
        except Exception as e:
            print(f"Error determining next ID: {e}")
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

        print("The result of the table:")
        print(tb1)

        answer = input("Do you want to save this table? (y/n): ").strip().lower()
        if answer == "y":
            try:
                bdb.save(tb1)
                print("Table saved successfully.")
                pause_and_clean(3)
            except Exception:
                print(f"Error saving table: {Exception}")
                pause_and_clean(3)
        elif answer == "n":
            print("You chose not to save this table.")
            pause_and_clean(1.5)
        else:
            print("Choose a correct option (y/n).")
            pause_and_clean(1.5)

    except Exception:
        print(f"An unexpected error occurred: {Exception}")

if __name__ == "__main__":
    add_names_to_db()
