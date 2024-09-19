# DB_manage/funtions/common/db_utils.py

import BivittatusDB as bdb

def initialize_database(db_name):
    """
    Initializes a database using the BivittatusDB (bdb) library.
    
    Args:
        db_name (str): The name of the database to initialize.
    
    Returns:
        object: The initialized database instance, or None if an error occurred.
    """
    try:
        # Inicializar la base de datos usando la función 'init()'
        test_db = bdb.database(db_name).init()
        print(f"Database '{db_name}' successfully initialized.")
        return test_db
    except Exception as e:
        print(f"Error initializing database '{db_name}': {e}")
        return None

def load_existing_table(db_name, table_name):
    """
    Loads an existing table from an initialized database instance.
    
    Args:
        db_name (str): The name of the database.
        table_name (str): The name of the table to load.
    
    Returns:
        object: The loaded table, or None if an error occurred.
    """
    try:
        # Inicializar la base de datos
        db_instance = initialize_database(db_name)
        if db_instance is None:
            raise ValueError("Failed to initialize the database.")
        
        # Cargar la tabla desde la base de datos
        tb1 = db_instance.load_table(table_name)
        print(f"Table '{table_name}' successfully loaded.")
        return tb1
    except Exception as e:
        print(f"Error loading table '{table_name}': {e}")
        return None
