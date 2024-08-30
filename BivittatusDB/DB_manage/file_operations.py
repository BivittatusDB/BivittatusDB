import os

def get_files_with_extension(db_directory, extension=".pydb"):
    """
    Lists all files in the database directory with a given extension.

    :param db_directory: Path to the database directory.
    :param extension: File extension to filter by. Default is '.pydb'.
    :return: List of file names with the specified extension in the database directory.
    """
    try:
        # Ensure the directory exists and is accessible
        if not os.path.isdir(db_directory):
            print(f"The directory '{db_directory}' does not exist or is not a directory.")
            return []

        # Get the list of files in the directory with the specified extension
        files = [f for f in os.listdir(db_directory) if f.endswith(extension)]
        return files

    except PermissionError:
        print(f"You do not have permission to access the directory '{db_directory}'.")
        return []
    except Exception as e:
        print(f"An error occurred while listing the files: {e}")
        return []
