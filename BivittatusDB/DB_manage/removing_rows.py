import BivittatusDB as bdb

def remove_rows():
    try:
        # Ask if you want to load an existing database
        db_choice = input("Do you want to load an existing database (y/n):").strip().lower()

        if db_choice == "y":
            db_name = input("Enter the name of the database directory: ").strip()
            table_name = input("Enter the name of the table you want to load: ").strip()

            try:
                # Load the database and the table
                test_db = bdb.database(db_name).init()
                tb1 = test_db.load_table(table_name)
                print(f"Table ‘{table_name}’ successfully loaded.")
                print(tb1)
            except Exception as e:
                print(f"Error loading table: {e}")
                return

        elif db_choice == "n":
            print("The option to create a new database or table is not implemented.")
            return

        else:
            print("Invalid option. Exiting.")
            return

        while True:
            # Request value to delete in the fixed column
            value_to_delete = input("Enter the value you wish to delete in the ‘name’ column (or ‘exit’ to exit): ").strip()
            if value_to_delete.lower() == 'exit':
                break

            # Attempt to delete rows corresponding to the value entered
            try:
                tb1["name"] - value_to_delete
                print(f"Filas con el valor '{value_to_delete}' en la columna 'name' eliminadas exitosamente.")
            except AttributeError:
                print(f"El objeto 'table' no tiene el método 'remove_rows'.")
            except Exception as e:
                print(f"Error al eliminar filas: {e}")

        print("Final table result:")
        print(tb1)

        while True:            
            answer = input("Do you want to save this table (y/n)? ").strip().lower()
            if answer == "y":
                try:
                    bdb.save(tb1)
                    print("Table successfully saved.")
                except Exception as e:
                    print(f"Error saving the table: {e}")
                break
            elif answer == "n":
                print("You have chosen not to save the table.")
                break
            else:
                print("Please choose one correct option (y/n).")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    remove_rows()