from db_connection_manager import DbConnectionManager

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
        while True:
            print("\n--- Admin Menu ---")
            print("1. Create Estate Agent")
            print("2. Update Estate Agent")
            print("3. Delete Estate Agent")
            print("4. Back to Main Menu")
            choice = input("Choose an option: ")

            if choice == "1":
                self.create_estate_agent()
            elif choice == "2":
                self.update_estate_agent()
            elif choice == "3":
                self.delete_estate_agent()
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")

    def create_estate_agent(self):
        print("\n--- Create New Estate Agent ---")
        name = input("Name: ")
        address = input("Address: ")
        login_name = input("Login Name: ")
        login_password = input("Login Password: ")

        cur = self.db.cursor()
        try:
            cur.execute(
                """
                INSERT INTO estate_agent (name, address, login_name, login_password)
                VALUES (%s, %s, %s, %s)
                """,
                (name, address, login_name, login_password)
            )
            self.db.commit()
            print("\nEstate agent created successfully.")
        except Exception as e:
            print(f"\nError creating estate agent: {e}")
            self.db.rollback()
        finally:
            cur.close()

    def update_estate_agent(self):
        print("\n--- Update Estate Agent ---")
        agent_id = input("Enter the ID of the agent to update: ")
        new_name = input("New Name: ")
        new_address = input("New Address: ")
        new_password = input("New Password: ")

        cur = self.db.cursor()
        try:
            cur.execute(
                """
                UPDATE estate_agent
                SET name = %s, address = %s, login_password = %s
                WHERE id = %s
                """,
                (new_name, new_address, new_password, agent_id)
            )
            self.db.commit()
            print("\nEstate agent updated successfully.")
        except Exception as e:
            print(f"\nError updating estate agent: {e}")
            self.db.rollback()
        finally:
            cur.close()

    def delete_estate_agent(self):
        print("\n--- Delete Estate Agent ---")
        agent_id = input("Enter the ID of the agent to delete: ")

        cur = self.db.cursor()
        try:
            cur.execute(
                """
                DELETE FROM estate_agent
                WHERE id = %s
                """,
                (agent_id,)
            )
            self.db.commit()
            print("\nEstate agent deleted successfully.")
        except Exception as e:
            print(f"\nError deleting estate agent: {e}")
            self.db.rollback()
        finally:
            cur.close()
