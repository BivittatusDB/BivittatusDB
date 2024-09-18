import BivittatusDB as bdb
from bdb_aggregate import delay

def save_table(tb1):
    answer = input("Do you want to save this table? (y/n): ").strip().lower()
    if answer == "y":
        try:
            bdb.save(tb1)
            print("Table saved successfully.")
            delay(1.5)
        except Exception as e:
            print(f"Error saving table: {e}")
    elif answer == "n":
        print("You chose not to save this table.")
        delay(2)
    else:
        print("Choose a correct option (y/n).")