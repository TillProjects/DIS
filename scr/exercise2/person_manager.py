from db_connection_manager import db_connection_manager

class PersonManager:
    def __init__(self):
        self.db = db_connection_manager.get_instance().get_connection()

    def person_menu(self):
        while True:
            print("\n--- Person Management ---")
            print("1. Create Person")
            print("2. Update Person")
            print("3. Delete Person")
            print("4. Back")
            choice = input("Choose an option: ")

            if choice == "1":
                self.create_person()
            elif choice == "2":
                self.update_person()
            elif choice == "3":
                self.delete_person()
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")

    def create_person(self):
        print("\n--- Create New Person ---")
        first_name = input("First Name: ")
        surname = input("Surname: ")
        address = input("Address: ")

        cur = self.db.cursor()
        try:
            cur.execute(
                """
                INSERT INTO person (first_name, surname, address)
                VALUES (%s, %s, %s)
                """,
                (first_name, surname, address)
            )
            self.db.commit()
            print("\nPerson created successfully.")
        except Exception as e:
            print(f"\nError creating person: {e}")
            self.db.rollback()
        finally:
            cur.close()

    def update_person(self):
        print("\n--- Update Person ---")
        person_id = input("Enter the ID of the person to update: ")
        first_name = input("New First Name: ")
        surname = input("New Surname: ")
        address = input("New Address: ")

        cur = self.db.cursor()
        try:
            cur.execute(
                """
                UPDATE person
                SET first_name = %s, surname = %s, address = %s
                WHERE id = %s
                """,
                (first_name, surname, address, person_id)
            )
            self.db.commit()
            print("\nPerson updated successfully.")
        except Exception as e:
            print(f"\nError updating person: {e}")
            self.db.rollback()
        finally:
            cur.close()

    def delete_person(self):
        print("\n--- Delete Person ---")
        person_id = input("Enter the ID of the person to delete: ")

        cur = self.db.cursor()
        try:
            cur.execute(
                """
                DELETE FROM person
                WHERE id = %s
                """,
                (person_id,)
            )
            self.db.commit()
            print("\nPerson deleted successfully.")
        except Exception as e:
            print(f"\nError deleting person: {e}")
            self.db.rollback()
        finally:
            cur.close()
