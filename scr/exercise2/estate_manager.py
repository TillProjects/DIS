from db_connection_manager import DbConnectionManager
from exercise2.contract_manager import ContractManager
from exercise2.person_manager import PersonManager
from utils.db_helpers import execute_query, menu


class EstateManager:
    def __init__(self):
        self.db = DbConnectionManager.get_instance().get_connection()
        self.current_agent_id = None

    def agent_login(self):
        print("\n--- Estate Agent Login ---")
        login_name = input("Login Name: ")
        login_password = input("Login Password: ")

        query = """
            SELECT id FROM estate_agent
            WHERE login_name = %s AND login_password = %s
        """
        result = execute_query(self.db, query, (login_name, login_password), fetch=True)
        print(result)

        if result:
            self.current_agent_id = result[0][0]
            print("\nAgent login successful.")
            self.estate_menu()
        else:
            print("\nInvalid login credentials.")

    def estate_menu(self):
        while True:
            menu(
                "Estate Management",
                [
                    ("Create Apartment", self.create_apartment),
                    ("Create House", self.create_house),
                    ("Update Apartment", self.update_apartment),
                    ("Update House", self.update_house),
                    ("Delete Apartment", self.delete_apartment),
                    ("Delete House", self.delete_house),
                    ("Manage Contracts", self.open_contract_manager),
                    ("Manage Persons", self.open_person_manager),
                    ("Logout", self.logout),
                ],
            )

    def logout(self):
        self.current_agent_id = None
        print("\nLogged out.")

    def create_apartment(self):
        print("\n--- Create New Apartment ---")
        data = {
            "city": input("City: "),
            "postal_code": input("Postal Code: "),
            "street": input("Street: "),
            "street_number": input("Street Number: "),
            "square_area": input("Square Area: "),
            "floor": input("Floor: "),
            "rent": input("Rent: "),
            "rooms": input("Rooms: "),
            "has_balcony": input("Has Balcony (true/false): ").strip().lower()
            == "true",
            "has_built_in_kitchen": input("Has Built-in Kitchen (true/false): ")
            .strip()
            .lower()
            == "true",
            "manager": self.current_agent_id,
        }

        query = """
                INSERT INTO apartment (city, postal_code, street, street_number, square_area, floor, rent, rooms,
                                       has_balcony, has_built_in_kitchen, manager)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
        execute_query(self.db, query, tuple(data.values()))
        print("\nApartment created successfully.")

    def create_house(self):
        print("\n--- Create New House ---")
        data = {
            "city": input("City: "),
            "postal_code": input("Postal Code: "),
            "street": input("Street: "),
            "street_number": input("Street Number: "),
            "square_area": input("Square Area: "),
            "floors": input("Floors: "),
            "price": input("Price: "),
            "has_garden": input("Has Garden (true/false): ").strip().lower() == "true",
            "manager": self.current_agent_id,
        }

        query = """
                INSERT INTO house (city, postal_code, street, street_number, square_area, floors, price, has_garden, manager)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
        execute_query(self.db, query, tuple(data.values()))
        print("\nHouse created successfully.")


    def update_apartment(self):
        from utils.db_helpers import prompt_with_default

        print("\n--- Update Apartment ---")
        apartment_id = input("Enter the ID of the apartment to update: ")

        query = """
                SELECT city, postal_code, street, street_number, square_area, floor, rent, rooms,
                       has_balcony, has_built_in_kitchen, manager
                FROM apartment
                WHERE id = %s AND manager = %s
            """
        apartment = execute_query(
            self.db, query, (apartment_id, self.current_agent_id), fetch=True
        )

        if not apartment:
            print("Apartment not found or you are not the manager.")
            return

        apartment = apartment[0]
        columns = [
            "city",
            "postal_code",
            "street",
            "street_number",
            "square_area",
            "floor",
            "rent",
            "rooms",
            "has_balcony",
            "has_built_in_kitchen",
            "manager",
        ]

        updated_values = []
        for i, col in enumerate(columns):
            old = apartment[i]
            new = prompt_with_default(col, old)

            if col in ["square_area", "floor", "rent", "rooms", "manager"]:
                updated_values.append(int(new))
            elif col in ["has_balcony", "has_built_in_kitchen"]:
                updated_values.append(str(new).lower() == "true")
            else:
                updated_values.append(new)

        update_query = f"""
                UPDATE apartment
                SET {', '.join(f"{col} = %s" for col in columns)}
                WHERE id = %s
            """
        execute_query(self.db, update_query, (*updated_values, apartment_id))
        print("\nApartment updated successfully.")


    def update_house(self):
        from utils.db_helpers import prompt_with_default

        print("\n--- Update House ---")
        house_id = input("Enter the ID of the house to update: ")

        query = """
                SELECT city, postal_code, street, street_number, square_area, floors, price, has_garden, manager
                FROM house
                WHERE id = %s AND manager = %s
            """
        house = execute_query(self.db, query, (house_id, self.current_agent_id), fetch=True)

        if not house:
            print("House not found or you are not the manager.")
            return

        house = house[0]
        columns = [
            "city",
            "postal_code",
            "street",
            "street_number",
            "square_area",
            "floors",
            "price",
            "has_garden",
            "manager",
        ]

        updated_values = []
        for i, col in enumerate(columns):
            old = house[i]
            new = prompt_with_default(col, old)

            if col in ["square_area", "floors", "manager"]:
                updated_values.append(int(new))
            elif col == "price":
                updated_values.append(float(new))
            elif col == "has_garden":
                updated_values.append(str(new).lower() == "true")
            else:
                updated_values.append(new)

        update_query = f"""
                UPDATE house
                SET {', '.join(f"{col} = %s" for col in columns)}
                WHERE id = %s
            """
        execute_query(self.db, update_query, (*updated_values, house_id))
        print("\nHouse updated successfully.")



    def delete_apartment(self):
        print("\n--- Delete Apartment ---")
        apartment_id = input("Enter the ID of the apartment to delete: ")

        query = """
                DELETE FROM apartment
                WHERE id = %s AND manager = %s
            """
        execute_query(self.db, query, (apartment_id, self.current_agent_id))
        print("\nApartment deleted successfully.")


    def delete_house(self):
        print("\n--- Delete House ---")
        house_id = input("Enter the ID of the house to delete: ")

        query = """
                DELETE FROM house
                WHERE id = %s AND manager = %s
            """
        execute_query(self.db, query, (house_id, self.current_agent_id))
        print("\nHouse deleted successfully.")


    def open_contract_manager(self):
        contract_manager = ContractManager()
        contract_manager.contract_menu()

    def open_person_manager(self):
        person_manager = PersonManager()
        person_manager.person_menu()

