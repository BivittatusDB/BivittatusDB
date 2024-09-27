from DB_manage.funtions.common.common_db_operations import get_table_from_db
from DB_manage.funtions.adding.table_utils import add_names_to_table
from DB_manage.funtions.common.saving import save_table

def add_names_to_db():
    try:
        tb1 = get_table_from_db()
        if tb1 is None:
            return

        add_names_to_table(tb1)
        print("The result of the table:")
        print(tb1)
        save_table(tb1)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    add_names_to_db()
