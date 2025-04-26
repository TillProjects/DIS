from auth import Auth
from estate_manager import EstateManager


def main():
    while True:
        print("\n=== Real Estate Management System ===")
        print("1. Admin Login (Manage Estate Agents)")
        print("2. Estate Agent Login (Manage Estates, Persons, Contracts)")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            auth = Auth()
            auth.admin_login()
        elif choice == "2":
            estate_manager = EstateManager()
            estate_manager.agent_login()
        elif choice == "3":
            print("\nGoodbye.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
