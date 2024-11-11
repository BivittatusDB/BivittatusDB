import os

def list_pydb(db_directory):
    """List .pydb files in the specified directory.

    Args:
        db_directory (str): The directory to check for .pydb files.

    Returns:
        tuple: A tuple containing the directory and a list of .pydb files, or an empty list if none found.
    """
    # Check if the directory exists
    if not os.path.isdir(db_directory):
        print(f"Warning: The directory '{db_directory}' does not exist. Please create it before proceeding.")
        return db_directory, []  # Return the directory with an empty list if it doesn't exist

    try:
        # Lists the .pydb files in the directory
        tables = [f.replace('.pydb', '') for f in os.listdir(db_directory) if f.endswith('.pydb')]

        if not tables:
            print(f"No .pydb files were found in the directory: {db_directory}")
            return db_directory, []  # Return the directory with an empty list if no files are found

        return db_directory, tables
    except Exception as e:
        print(f"Error listing files in directory '{db_directory}': {e}")
        return None, []
