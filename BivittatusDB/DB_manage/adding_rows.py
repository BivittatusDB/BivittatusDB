import BivittatusDB as bdb
from bdb_aggregate import pause_and_clean
from DB_manage.file_operations import get_files_with_extension

def show_files_with_extension(db_directory, extension=".pydb"):
    files = get_files_with_extension(db_directory, extension)
    if files:
        print(f"Files with the '{extension}' extension in the database directory:")
        for file in files:
            print(file)
    else:
        print(f"There are no files with the '{extension}' extension in the database directory.")
    return files

def load_existing_table(db_directory):
    files = show_files_with_extension(db_directory)
    if not files:
        print("No files found to load. Exiting.")
        return None
    
    table_name = input("Enter the name of the table to load (without the .pydb extension): ").strip()
    if f"{table_name}.pydb" in files:
        try:
            test_db = bdb.database(db_directory).init()
            tb1 = test_db.load_table(table_name)
            print(f"Table '{table_name}' successfully loaded.")
            print(tb1)
            return tb1
        except Exception as e:
            print(f"Error loading table: {e}")
            return None
    else:
        print(f"Table '{table_name}' not found in the directory.")
        return None

def create_new_table(db_name):
    table_name = input("Enter a name for the new table: ").strip()
    try:
        test_db = bdb.database(db_name).init()
        tb1 = test_db.New_table(
            table_name, ("id", "name"), (int, str), "id"
        )
        print("New table created.")
        return tb1
    except Exception as e:
        print(f"Error creating table: {e}")
        return None

def add_names_to_table(tb1):
    next_id = (max(row[0] for row in tb1) + 1) if len(tb1) > 0 else 1
    while True:
        name = input("Enter a name to add to the table (or 'exit' to end): ").strip()
        if name.lower() == 'exit':
            break
        try:
            tb1 + (next_id, name)
            next_id += 1
            print(f"Successfully added name to table: {name}")
        except Exception as e:
            print(f"Error adding name to table: {e}")

def save_table(tb1):
    while True:
        answer = input("Do you want to save this table? (y/n): ").strip().lower()
        if answer == "y":
            try:
                bdb.save(tb1)
                print("Table saved successfully.")
                pause_and_clean(0.4)
                return
            except Exception as e:
                print(f"Error saving table: {e}")
        elif answer == "n":
            print("You chose not to save this table.")
            return
        else:
            print("Choose a correct option (y/n).")

def add_names_to_db():
    try:
        db_choice = input("Do you want to load an existing database (y) or create a new one (n)? ").strip().lower()
        db_directory = input("Enter the name of the database directory: ").strip()
        
        if db_choice == "y":
            tb1 = load_existing_table(db_directory)
            if tb1:
                add_names_to_table(tb1)
                save_table(tb1)
        
        elif db_choice == "n":
            db_name = input("Enter a name for your new database: ").strip()
            tb1 = create_new_table(db_name)
            if tb1:
                add_names_to_table(tb1)
                save_table(tb1)
        
        else:
            print("Invalid choice. Exiting.")
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    add_names_to_db()
