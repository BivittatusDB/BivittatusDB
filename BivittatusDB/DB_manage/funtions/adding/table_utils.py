from bdb_aggregate import pause_and_clean

def get_next_id(tb1):
    try:
        if len(tb1) > 0:
            return max(row[0] for row in tb1) + 1
        else:
            return 1
    except Exception as e:
        print(f"Error determining next ID: {e}")
        return None

def add_names_to_table(tb1):
    next_id = get_next_id(tb1)
    if next_id is None:
        return

    while True:
        pause_and_clean(0)
        print("The current table:")
        print(tb1)
        name = input("Enter a name to add to the table (or 'exit' to end): ").strip()
        if name.lower() == 'exit':
            pause_and_clean(0)
            break
        try:
            tb1 + (next_id, name)
            next_id += 1
        except Exception as e:
            print(f"Error adding name to table: {e}")
