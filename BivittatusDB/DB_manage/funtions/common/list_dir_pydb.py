from adding.user_interaction import get_db_and_table_names

def list_pydb():
    """
    Prompts the user to enter the database folder name and table name, and initializes the database.
    """
    while True:
        try:
            return get_db_and_table_names()
        except:
            continue
