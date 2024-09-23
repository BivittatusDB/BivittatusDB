from bdb_aggregate import pause_and_clean

def remove_rows_from_table(tb1):
    """
    Removes rows from a table based on user input.
    
    Args:
        tb1 (object): The table from which to remove rows.
    """
    while True:
        pause_and_clean(0)
        print(tb1)
        value_to_delete = input("Enter the value you wish to delete in the 'name' column (or 'exit' to exit): ").strip()
        if value_to_delete.lower() == 'exit':
            pause_and_clean(0)
            break

        try:
            tb1["name"] - value_to_delete
            print(f"Rows with value '{value_to_delete}' in column 'name' successfully deleted.")
        except AttributeError:
            print("The table object does not have a 'remove_rows' method.")
        except Exception as e:
            print(f"Error when deleting rows: {e}")
