import os
import BivittatusDB as bdb

def create_db_and_table():
    # Request user input
    db_directory = input("Enter the directory for the database: ").strip()
    table_name = input("Enter the name of the table: ").strip()

    # Validate inputs
    if not table_name:
        print("Table name cannot be empty.")
        return

    # Check and create the directory if it doesn't exist
    try:
        os.makedirs(db_directory, exist_ok=True)
        print(f"Directory '{db_directory}' is ready.")
    except Exception as e:
        print(f"Error creating directory '{db_directory}': {e.__class__.__name__} - {e}")
        return

    # Create the database and the table
    try:
        db_path = os.path.join(db_directory)  # Using the user-provided database name
        
        # Initialize the database using the init() function
        db = bdb.database(db_path).init()
        print(f"Database '{table_name}' successfully initialized.")
        
        # Create the new table
        table = db.New_table(
            table_name,
            ("id", "name"),
            (int(), str()),
            "id"
        )
        print(f"New table '{table_name}' created in database '{db_directory}'.")
        
        # Verification of table creation
        if table is not None:
            print("Table created successfully.")
        else:
            print("Table creation failed.")
    
    except Exception as e:
        print(f"Error creating table '{table_name}' in database '{db_directory}': {e.__class__.__name__} - {e}")

if __name__ == "__main__":
    create_db_and_table()
