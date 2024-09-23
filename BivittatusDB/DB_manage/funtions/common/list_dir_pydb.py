import os

def list_pydb(db_directory):
    """
    Lists the database files (.pydb) in the given directory.

    Args:
        db_directory (str): The directory of the database.

    Returns:
        tuple: (db_directory, tables) if the files are listed correctly,
               (None, []) on error.
    """
    try:
        # Check if the directory exists
        if not os.path.isdir(db_directory):
            raise FileNotFoundError(f"The directory '{db_directory}' does not exist.")

        print(f"Trying to list the files in the directory: {db_directory}")
        # Lists the .pydb files in the directory
        tables = [f.replace('.pydb', '') for f in os.listdir(db_directory) if f.endswith('.pydb')]

        if not tables:
            print(f"No .pydb files were found in the directory: {db_directory}")
            return db_directory, []  # Retorna el directorio con lista vacía si no hay archivos

        return db_directory, tables
    except Exception as e:
        print(f"Error listing files in directory '{db_directory}': {e}")
        return None, []
