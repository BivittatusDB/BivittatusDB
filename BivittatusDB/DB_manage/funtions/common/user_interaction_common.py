from bdb_aggregate import delay

def get_db_choice_common():
    """
    Asks the user if they want to load an existing database.
    
    Returns:
        str: 'y' for loading an existing database, 'n' for not loading.
    """
    while True:
        choice = input("Do you want to load an existing database (y/n): ").strip().lower()
        if choice in ['y']:
            return choice
        if choice in ['n']:
            print("Operation canceled.")
            delay(0.8)
            return None
        else:
            print("Invalid input. Please enter 'y'.")
