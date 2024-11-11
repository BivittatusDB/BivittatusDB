import json

def get_schema_name():
    """Prompt for the schema name."""
    return input("Enter the schema name: ")

def get_num_tables():
    """Prompt for the number of tables and validate the input."""
    while True:
        try:
            return int(input("How many tables do you want to create? "))
        except ValueError:
            print("Please enter a valid number.")

def get_table_name(index):
    """Prompt for the table name."""
    return input(f"Enter the name of table {index + 1}: ")

def get_num_columns(table_name):
    """Prompt for the number of columns in the table and validate the input."""
    while True:
        try:
            return int(input(f"How many columns will the table '{table_name}' have? "))
        except ValueError:
            print("Please enter a valid number.")

def get_column_info(table_name, column_index):
    """Prompt for the column name and data type."""
    column_name = input(f"Enter the name of column {column_index + 1} in '{table_name}': ")
    column_type = input(f"Enter the data type for '{column_name}' (e.g., int, str, float): ")
    return column_name, column_type

def get_primary_key(table_name, columns):
    """Prompt for the primary key column and validate the choice."""
    while True:
        primary_key = input(f"Enter the name of the primary key in '{table_name}': ")
        if primary_key in columns:
            return primary_key
        print(f"Invalid input. Please choose from the following columns: {columns}")

def get_foreign_keys(table_name, columns):
    """Prompt for foreign keys if any, and gather details."""
    foreign_keys = []
    add_foreign_key = input(f"Does the table '{table_name}' have a foreign key? (yes/no): ").strip().lower()
    
    if add_foreign_key == 'yes':
        while True:
            try:
                num_foreign_keys = int(input(f"How many foreign keys does '{table_name}' have? "))
                break
            except ValueError:
                print("Please enter a valid number.")
        
        for fk in range(num_foreign_keys):
            referenced_table = input("Enter the name of the referenced table: ")
            referenced_column = input("Enter the name of the referenced column in the referenced table: ")
            column_name = input("Enter the name of the column in this table that will be a foreign key: ")
            
            if column_name in columns:
                foreign_keys.append({
                    "column": column_name,
                    "referenced_table": referenced_table,
                    "referenced_column": referenced_column
                })
            else:
                print(f"The column '{column_name}' does not exist in '{table_name}' columns.")
    
    return foreign_keys

def create_table_structure(table_name):
    """Create the structure of a table by gathering columns, data types, primary key, and foreign keys."""
    num_columns = get_num_columns(table_name)
    
    columns = []
    data_types = []

    for j in range(num_columns):
        column_name, column_type = get_column_info(table_name, j)
        columns.append(column_name)
        data_types.append(column_type)

    primary_key = get_primary_key(table_name, columns)
    foreign_keys = get_foreign_keys(table_name, columns)

    return {
        "columns": columns,
        "data_types": data_types,
        "primary_key": primary_key,
        "foreign_keys": foreign_keys or []  # Use empty list if no foreign keys
    }

def main():
    # Gather schema and table information
    schema_name = get_schema_name()
    num_tables = get_num_tables()

    tables = {}
    for i in range(num_tables):
        table_name = get_table_name(i)
        tables[table_name] = create_table_structure(table_name)

    # Create and display the JSON
    data = {schema_name: tables}
    json_data = json.dumps(data, indent=4)
    print("\nGenerated JSON Schema:")
    print(json_data)

if __name__ == "__main__":
    main()
