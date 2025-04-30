from auth import Auth
from estate_manager import EstateManager
from utils.db_helpers import menu


def main():
    running = True

    def admin_login():
        Auth().admin_login()

    def agent_login():
        EstateManager().agent_login()

    def exit_program():
        nonlocal running
        print("\nGoodbye.")
        running = False

    while running:
        menu("Real Estate Management System", [
            ("Admin Login (Manage Estate Agents)", admin_login),
            ("Estate Agent Login (Manage Estates, Persons, Contracts)", agent_login),
            ("Exit", exit_program)
        ])


if __name__ == "__main__":
    main()
