from db_connection_manager import DbConnectionManager
from exercise2.contract_manager import ContractManager
from exercise2.person_manager import PersonManager


class EstateManager:
    def __init__(self):
        self.db = DbConnectionManager.get_instance().get_connection()
        self.current_agent_id = None

    def agent_login(self):
        print("\n--- Estate Agent Login ---")
        login_name = input("Login Name: ")
        login_password = input("Login Password: ")

        cur = self.db.cursor()
        try:
            cur.execute(
                """
                SELECT id FROM estate_agent
                WHERE login_name = %s AND login_password = %s
                """,
                (login_name, login_password),
            )
            result = cur.fetchone()
            if result:
                self.current_agent_id = result[0]
                print("\nAgent login successful.")
                self.estate_menu()
            else:
                print("\nInvalid login credentials.")
        except Exception as e:
            print(f"\nError during login: {e}")
        finally:
            cur.close()

    def estate_menu(self):
        while True:
            print("\n--- Estate Management ---")
            print("1. Create Apartment")
            print("2. Create House")
            print("3. Update Apartment")
            print("4. Update House")
            print("5. Delete Apartment")
            print("6. Delete House")
            print("7. Manage Contracts")
            print("8. Manage Persons")
            print("9. Logout")
            choice = input("Choose an option: ")

            if choice == "1":
                self.create_apartment()
            elif choice == "2":
                self.create_house()
            elif choice == "3":
                self.update_apartment()
            elif choice == "4":
                self.update_house()
            elif choice == "5":
                self.delete_apartment()
            elif choice == "6":
                self.delete_house()
            elif choice == "7":
                self.open_contract_manager()
            elif choice == "8":
                self.open_person_manager()
            elif choice == "9":
                self.current_agent_id = None
                print("\nLogged out.")
                break
            else:
                print("Invalid choice. Please try again.")

    def create_apartment(self):
        print("\n--- Create New Apartment ---")
        city = input("City: ")
        postal_code = input("Postal Code: ")
        street = input("Street: ")
        street_number = input("Street Number: ")
        square_area = input("Square Area: ")
        floor = input("Floor: ")
        rent = input("Rent: ")
        rooms = input("Rooms: ")
        has_balcony = input("Has Balcony (true/false): ").lower() == "true"
        has_built_in_kitchen = (
            input("Has Built-in Kitchen (true/false): ").lower() == "true"
        )

        cur = self.db.cursor()
        try:
            cur.execute(
                """
                INSERT INTO apartment (city, postal_code, street, street_number, square_area, floor, rent, rooms, has_balcony, has_built_in_kitchen, manager)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    city,
                    postal_code,
                    street,
                    street_number,
                    square_area,
                    floor,
                    rent,
                    rooms,
                    has_balcony,
                    has_built_in_kitchen,
                    self.current_agent_id,
                ),
            )
            self.db.commit()
            print("\nApartment created successfully.")
        except Exception as e:
            print(f"\nError creating apartment: {e}")
            self.db.rollback()
        finally:
            cur.close()

    def create_house(self):
        print("\n--- Create New House ---")
        city = input("City: ")
        postal_code = input("Postal Code: ")
        street = input("Street: ")
        street_number = input("Street Number: ")
        square_area = input("Square Area: ")
        floors = input("Floors: ")
        price = input("Price: ")
        has_garden = input("Has Garden (true/false): ").lower() == "true"

        cur = self.db.cursor()
        try:
            cur.execute(
                """
                INSERT INTO house (city, postal_code, street, street_number, square_area, floors, price, has_garden, manager)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    city,
                    postal_code,
                    street,
                    street_number,
                    square_area,
                    floors,
                    price,
                    has_garden,
                    self.current_agent_id,
                ),
            )
            self.db.commit()
            print("\nHouse created successfully.")
        except Exception as e:
            print(f"\nError creating house: {e}")
            self.db.rollback()
        finally:
            cur.close()

    def update_apartment(self):
        print("\n--- Update Apartment ---")
        apartment_id = input("Enter the ID of the apartment to update: ")

        cur = self.db.cursor()
        try:
            # Bestehende Werte holen
            cur.execute(
                """
                SELECT city, postal_code, street, street_number, square_area, floor, rent, rooms, has_balcony, has_built_in_kitchen, manager
                FROM apartment
                WHERE id = %s
            """,
                apartment_id,
            )
            apartment = cur.fetchone()

            if not apartment:
                print("Apartment not found or you are not the manager.")
                return

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
            for index, column in enumerate(columns):
                old_value = apartment[index]
                new_value = input(f"{column} [{old_value}]: ")
                if new_value == "":
                    updated_values.append(old_value)
                else:
                    if column in ["square_area", "floor", "rent", "rooms", "manager"]:
                        updated_values.append(int(new_value))
                    elif column in ["has_balcony", "has_built_in_kitchen"]:
                        updated_values.append(new_value.lower() == "true")
                    else:
                        updated_values.append(new_value)

            # Update Query
            cur.execute(
                f"""
                UPDATE apartment
                SET city = %s, postal_code = %s, street = %s, street_number = %s, square_area = %s,
                    floor = %s, rent = %s, rooms = %s, has_balcony = %s, has_built_in_kitchen = %s, manager = %s
                WHERE id = %s
            """,
                (*updated_values, apartment_id),
            )

            self.db.commit()
            print("\nApartment updated successfully.")
        except Exception as e:
            print(f"\nError updating apartment: {e}")
            self.db.rollback()
        finally:
            cur.close()

    def update_house(self):
        print("\n--- Update House ---")
        house_id = input("Enter the ID of the house to update: ")

        cur = self.db.cursor()
        try:
            cur.execute(
                """
                SELECT city, postal_code, street, street_number, square_area, floors, price, has_garden, manager
                FROM house
                WHERE id = %s
            """,
                house_id,
            )
            house = cur.fetchone()

            if not house:
                print("House not found or you are not the manager.")
                return

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
            for index, column in enumerate(columns):
                old_value = house[index]
                new_value = input(f"{column} [{old_value}]: ")
                if new_value == "":
                    updated_values.append(old_value)
                else:
                    if column in ["square_area", "floors", "price", "manager"]:
                        updated_values.append(
                            float(new_value) if column == "price" else int(new_value)
                        )
                    elif column in ["has_garden"]:
                        updated_values.append(new_value.lower() == "true")
                    else:
                        updated_values.append(new_value)

            cur.execute(
                """
                UPDATE house
                SET city = %s, postal_code = %s, street = %s, street_number = %s, square_area = %s,
                    floors = %s, price = %s, has_garden = %s, manager = %s
                WHERE id = %s
            """,
                (*updated_values, house_id),
            )

            self.db.commit()
            print("\nHouse updated successfully.")
        except Exception as e:
            print(f"\nError updating house: {e}")
            self.db.rollback()
        finally:
            cur.close()

    def delete_apartment(self):
        print("\n--- Delete Apartment ---")
        apartment_id = input("Enter the ID of the apartment to delete: ")

        cur = self.db.cursor()
        try:
            cur.execute(
                """
                DELETE FROM apartment
                WHERE id = %s AND manager = %s
                """,
                (apartment_id, self.current_agent_id),
            )
            self.db.commit()
            print("\nApartment deleted successfully.")
        except Exception as e:
            print(f"\nError deleting apartment: {e}")
            self.db.rollback()
        finally:
            cur.close()

    def delete_house(self):
        print("\n--- Delete House ---")
        house_id = input("Enter the ID of the house to delete: ")

        cur = self.db.cursor()
        try:
            cur.execute(
                """
                DELETE FROM house
                WHERE id = %s AND manager = %s
                """,
                (house_id, self.current_agent_id),
            )
            self.db.commit()
            print("\nHouse deleted successfully.")
        except Exception as e:
            print(f"\nError deleting house: {e}")
            self.db.rollback()
        finally:
            cur.close()

    def open_contract_manager(self):
        contract_manager = ContractManager()
        contract_manager.contract_menu()

    def open_person_manager(self):
        person_manager = PersonManager()
        person_manager.person_menu()
