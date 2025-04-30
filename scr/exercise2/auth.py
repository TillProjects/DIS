from db_connection_manager import DbConnectionManager
from utils.db_helpers import execute_query, menu

class Auth:
    ADMIN_PASSWORD = "admin123"

    def __init__(self):
        self.db = DbConnectionManager.get_instance().get_connection()

    def admin_login(self):
        password = input("\nEnter admin password: ")
        if password == self.ADMIN_PASSWORD:
            print("\nAdmin login successful.")
            self.admin_menu()
        else:
            print("\nIncorrect password.")

    def admin_menu(self):
        menu("Admin Menu", [
            ("Create Estate Agent", self.create_estate_agent),
            ("Update Estate Agent", self.update_estate_agent),
            ("Delete Estate Agent", self.delete_estate_agent),
            ("Back to Main Menu", lambda: None)
        ])

    def create_estate_agent(self):
        print("\n--- Create New Estate Agent ---")
        data = {
            "name": input("Name: "),
            "address": input("Address: "),
            "login_name": input("Login Name: "),
            "login_password": input("Login Password: "),
        }

        query = """
                INSERT INTO estate_agent (name, address, login_name, login_password)
                VALUES (%s, %s, %s, %s)
            """
        execute_query(self.db, query, tuple(data.values()))
        print("\nEstate agent created successfully.")

    def update_estate_agent(self):
        print("\n--- Update Estate Agent ---")
        agent_id = input("Enter the ID of the agent to update: ")

        data = {
            "name": input("New Name: "),
            "address": input("New Address: "),
            "login_password": input("New Password: ")
        }

        query = """
            UPDATE estate_agent
            SET name = %s, address = %s, login_password = %s
            WHERE id = %s
        """
        execute_query(self.db, query, (*data.values(), agent_id))
        print("\nEstate agent updated successfully.")

    def delete_estate_agent(self):
        print("\n--- Delete Estate Agent ---")
        data = {
            "id": input("Enter the ID of the agent to delete: ")
        }

        query = "DELETE FROM estate_agent WHERE id = %s"
        execute_query(self.db, query, (data["id"],))
        print("\nEstate agent deleted successfully.")

