# Be careful manipulating this module; it works well for this example of a table.
import time
import BivittatusDB as bdb

def add_names_to_db():
    # Initialize the database
    test_db = bdb.database("test").init()

    # Create a new table
    tb1 = test_db.New_table(
        "table1",  # Name of the table
        ("id", "name"),  # Columns are named "id" and "name"
        (int(), str()),  # id contains int, and name contains str
        "id"  # id will be the primary key
    )

    # Initialize id
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