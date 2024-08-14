from bdb_aggregate import pause_and_clean
from DB_manage.adding_rows import add_names_to_db
from DB_manage.table_view import use_table
from DB_manage.update_table import update_tb

def display_menu():
    menu_options = [
        "Option 1: Use table",
        "Option 2: Insert values in table",
        "Option 3: Delete values in the table",
        "Option 4: Update values in the table",
        "Option 5: Print metadata",
        "Option 6: Exit"
    ]
    pause_and_clean(0)  # Llama a la función para limpiar la pantalla antes de mostrar el menú
    print("What do you want to do?")
    for option in menu_options:
        print(option)

def handle_use_table():
    try:
        use_table()
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        pause_and_clean(0.4)

def handle_option(option):
    options_map = {
        "1": handle_use_table,
        "2": lambda: (pause_and_clean(0), add_names_to_db()),
        "3": lambda: (print("This option is not yet implemented."), pause_and_clean(1)),
        "4": lambda: (pause_and_clean(0.4), update_tb()),
        "5": lambda: (print("Module not available"), pause_and_clean(1)),
        "6": lambda: (print("Exiting...."), pause_and_clean(0.4), False)
    }
    
    action = options_map.get(option)
    if action:
        result = action()
        return result if result is not None else True
    else:
        print("Incorrect option")
        pause_and_clean(0.8)
        return True

def main_menu():
    try:
        while True:
            display_menu()
            option = input("Please enter an option: ")
            if not handle_option(option):
                break
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt detected. Exiting...")
        pause_and_clean(0.8)

if __name__ == "__main__":
    main_menu()
