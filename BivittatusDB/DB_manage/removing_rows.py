from DB_manage.funtions.common.common_db_operations import get_table_from_db
from DB_manage.funtions.removing.rm_rows import remove_rows_from_table
from DB_manage.funtions.common.saving import save_table

def remove_rows():
    try:
        tb1 = get_table_from_db()
        if tb1 is None:
            return

        remove_rows_from_table(tb1)
        print("Final table result:")
        print(tb1)
        save_table(tb1)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    remove_rows()
