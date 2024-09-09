import BivittatusDB as bdb

# WIP Module

# Drop pre-existing databases (for best practice and to prevent errors)
try:
    bdb.drop("test")
except Exception as e:
    print(f"Error dropping database: {e}")

# Initialize the database
test_db = bdb.database("test").init()

# Create a new table
try:
    tb1 = test_db.new_table(
        "example_table",
        ("id", "name"),
        (int, str),
        "id"
    )
    print("Table 'example_table' created.")
except Exception as e:
    print(f"Error creating table: {e}")

# Write data to the table using the print function with the file argument
try:
    print((3, "Cindy"), file=tb1)  # Write a single row
except Exception as e:
    print(f"Error writing to table: {e}")

# Add more data to the table
try:
    tb1.write((1, "Alice"))  # Add another row
    tb1.write((2, "Bob"))    # Add another row
    print("Data added to table.")
except Exception as e:
    print(f"Error adding data to table: {e}")

# Read data from the table
try:
    print("All data in table:")
    print(tb1.read())  # Read all data from the table
except Exception as e:
    print(f"Error reading data: {e}")

# Read one line at a time
try:
    print(tb1.readline())  # Read one line
    print(tb1.readline())  # Read another line
    print(tb1.readline())  # Read yet another line
except Exception as e:
    print(f"Error reading line: {e}")

# Read a specific line
try:
    print(tb1.readline(1))  # Read a specific line
except Exception as e:
    print(f"Error reading specific line: {e}")

# Change position (simulating file position operations)
try:
    tb1.seek(0, 0)  # Seek to the beginning of the table
    print("Position after seek:", tb1.tell())  # Get current position
except Exception as e:
    print(f"Error seeking position: {e}")

# Read several lines starting at current position
try:
    print("Lines read from current position:")
    print(tb1.readlines(2))  # Read a number of lines starting from current position
except Exception as e:
    print(f"Error reading lines: {e}")

# Write to disk (flush the data to disk)
try:
    tb1.flush()
    print("Data flushed to disk.")
except Exception as e:
    print(f"Error flushing data: {e}")
