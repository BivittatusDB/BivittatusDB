# Be careful manipulating this module; it works well for this example of a table.
import time
import BivittatusDB as bdb

def add_names_to_db():
    # Ask if you want to load an existing database or create a new database
    db_choice = input("Do you want to load an existing database (y/n): ").strip().lower()

    if db_choice == "y":
        db_name = input("Enter the name of the database folder: ")
        table_name = input("Enter the name of the table you want to load: ")
        test_db = bdb.database(db_name).init()  # Load existing database
        tb1 = test_db.load_table(table_name)  # Load existing table
        print(f"Table ‘{table_name}’ successfully loaded.")
    else:
        # Attempt to create a new database
        db_name = input("Enter a name for your DB: ")
        test_db = bdb.database(db_name).init()
        table_name = input("Enter a name for the new table: ")  # Ask the user for a table name
        tb1 = test_db.New_table(
            table_name,  # Table name
            ("id", "name"),  # The columns are called ‘id’ and ‘name’
            (int(), str()),  # id contains int, and name contains str
            "id"  # id will be the primary key
        )
        print("New table created.")

    # Get the last id in the table to avoid duplicates
    if len(tb1) > 0:
        id = max(row[0] for row in tb1) + 1  # Access the first element of each row to get the id
    else:
        id = 1

    while True:
        # Ask for a name
        name = input("Enter a name to add to the table (or 'exit' to end): ")

        # Break loop if user wants to quit
        if name.lower() == 'exit':
            break

        # Add row to table
        tb1 + (id, name)
        
        # Increment id
        id += 1

    print("The result of the table:")
    print(tb1)

    while True:
        answer = input("Do you want to save this table? (y/n): ").strip().lower()
        if answer == "y":
            bdb.save(tb1)  # Save the table using bdb.save function
            print("Table saved successfully.")
            time.sleep(0.8)
            break  # Exit the loop after saving the table
        elif answer == "n":
            print("You chose not to save this table.")
            break  # Exit the loop after deciding not to save the table
        else:
            print("Choose a correct option (y/n).")