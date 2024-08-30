# display_files.py
from file_operations import get_files_with_extension

def show_files_with_extension(directory, extension=".pydb"):
    """
    Prints the files with the specified extension in the directory.

    :param directory: Path to the directory.
    :param extension: File extension to filter by. Default is '.pydb'.
    """
    # List files in the directory with the specified extension
    files = get_files_with_extension(directory, extension)

    if not files:
        print(f"There are no files with the '{extension}' extension in the directory.")
    else:
        print(f"Files with the '{extension}' extension in the directory:")
        for file in files:
            print(file)

# Example usage
if __name__ == "__main__":
    directory = input("Enter the name of the directory: ").strip()
    show_files_with_extension(directory)
