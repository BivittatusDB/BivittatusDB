#Needs a fix (double n to cancel)
def get_db_choice():
    while True:
        choice = input("Do you want to load an existing database (y/n): ").strip().lower()
        if choice == 'n':
            print("Operation canceled.")
            return None  # Return None to indicate cancellation
        elif choice == 'y':
            return 'y'  # Return 'y' to indicate loading an existing database
        print("Invalid input. Please enter 'y' or 'n'.")
