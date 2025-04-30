from db_connection_manager import DbConnectionManager
from utils.db_helpers import execute_query

class PersonManager:
    def __init__(self):
        self.db = DbConnectionManager.get_instance().get_connection()

    def person_menu(self):
        while True:
            print("\n--- Person Management ---")
            print("1. Create Person")
            print("2. Update Person")
            print("3. Delete Person")
            print("4. Back")
            choice = input("Choose an option: ")

            match choice:
                case "1":
                    self.create_person()
                case "2":
                    self.update_person()
                case "3":
                    self.delete_person()
                case "4":
                    break
                case _:
                    print("Invalid choice. Please try again.")

    def create_person(self):
        print("\n--- Create New Person ---")
        data = {
            "first_name": input("First Name: "),
            "surname": input("Surname: "),
            "address": input("Address: ")
        }

        query = """
            INSERT INTO person (first_name, surname, address)
            VALUES (%s, %s, %s)
        """
        execute_query(self.db, query, tuple(data.values()))
        print("\nPerson created successfully.")

    def update_person(self):
        print("\n--- Update Person ---")
        person_id = input("Enter the ID of the person to update: ")
        data = {
            "first_name": input("New First Name: "),
            "surname": input("New Surname: "),
            "address": input("New Address: ")
        }

        query = """
            UPDATE person
            SET first_name = %s, surname = %s, address = %s
            WHERE id = %s
        """
        execute_query(self.db, query, (*data.values(), person_id))
        print("\nPerson updated successfully.")

    def delete_person(self):
        print("\n--- Delete Person ---")
        person_id = input("Enter the ID of the person to delete: ")

        query = "DELETE FROM person WHERE id = %s"
        execute_query(self.db, query, (person_id,))
        print("\nPerson deleted successfully.")
