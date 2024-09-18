import BivittatusDB as bdb

def load_existing_table(db_name, table_name):
    try:
        test_db = bdb.database(db_name).init()
        tb1 = test_db.load_table(table_name)
        print(f"Table '{table_name}' successfully loaded.")
        #delay(1)
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
