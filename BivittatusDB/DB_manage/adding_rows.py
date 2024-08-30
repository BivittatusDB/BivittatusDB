import BivittatusDB as bdb

def add_names_to_db():
    try:
        # Ask if you want to load an existing database or create a new database
        db_choice = input("Do you want to load an existing database (y/n): ").strip().lower()

        if db_choice == "y":
            db_name = input("Enter the name of the database folder: ").strip()
            table_name = input("Enter the name of the table you want to load: ").strip()

            try:
                test_db = bdb.database(db_name).init()  # Load existing database
                tb1 = test_db.load_table(table_name)  # Load existing table
                print(f"Table '{table_name}' successfully loaded.")
            except Exception as e:
                print(f"Error loading table: {e}")
                return

        elif db_choice == "n":
            db_name = input("Enter a name for your DB: ").strip()
            table_name = input("Enter a name for the new table: ").strip()

            try:
                test_db = bdb.database(db_name).init()
                tb1 = test_db.New_table(
                    table_name,  # Table name
                    ("id", "name"),  # The columns are called 'id' and 'name'
                    (int(), str()),  # id contains int, and name contains str
                    "id"  # id will be the primary key
                )
                print("New table created.")
            except Exception as e:
                print(f"Error creating table: {e}")
                return
        else:
            print("Invalid choice. Exiting.")
            return

        # Get the last id in the table to avoid duplicates
        try:
            if len(tb1) > 0:
                id = max(row[0] for row in tb1) + 1  # Access the first element of each row to get the id
            else:
                id = 1
        except Exception as e:
            print(f"Error determining next ID: {e}")
            return

        while True:
            # Ask for a name
            name = input("Enter a name to add to the table (or 'exit' to end): ").strip()

            # Break loop if user wants to quit
            if name.lower() == 'exit':
                break

            # Add row to table
            try:
                tb1 + (id, name)
                # Increment id
                id += 1
            except Exception as e:
                print(f"Error adding name to table: {e}")

        print("The result of the table:")
        print(tb1)

        while True:
            answer = input("Do you want to save this table? (y/n): ").strip().lower()
            if answer == "y":
                try:
                    bdb.save(tb1)  # Save the table using bdb.save function
                    print("Table saved successfully.")
                except Exception as e:
                    print(f"Error saving table: {e}")
                finally:
                    break  # Exit the loop after saving or if an error occurs
            elif answer == "n":
                print("You chose not to save this table.")
            else:
                print("Choose a correct option (y/n).")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    add_names_to_db()