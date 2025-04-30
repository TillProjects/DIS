from db_connection_manager import DbConnectionManager
from utils.db_helpers import execute_query, menu

class ContractManager:
    def __init__(self):
        self.db = DbConnectionManager.get_instance().get_connection()

    def contract_menu(self):
        menu("Contract Management", [
            ("Create Tenancy Contract (Apartment)", self.create_tenancy_contract),
            ("Create Purchase Contract (House)", self.create_purchase_contract),
            ("List Contracts", self.list_contracts),
            ("Back", lambda: None)
        ])

    def create_tenancy_contract(self):
        print("\n--- Create Tenancy Contract ---")
        data = {
            "date": input("Contract Date (YYYY-MM-DD): "),
            "place": input("Place: "),
            "start_date": input("Start Date (YYYY-MM-DD): "),
            "duration": input("Duration (months): "),
            "additional_costs": input("Additional Costs: "),
            "person_id": input("Person ID: "),
            "apartment_id": input("Apartment ID: ")
        }

        query = """
            INSERT INTO tenancy_contract (date, place, start_date, duration, additional_costs, person, apartment)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        execute_query(self.db, query, tuple(data.values()))
        print("\nTenancy contract created successfully.")

    def create_purchase_contract(self):
        print("\n--- Create Purchase Contract ---")
        data = {
            "date": input("Contract Date (YYYY-MM-DD): "),
            "place": input("Place: "),
            "no_of_installments": input("Number of Installments: "),
            "interest_rate": input("Interest Rate (%): "),
            "person_id": input("Person ID: "),
            "house_id": input("House ID: ")
        }

        query = """
            INSERT INTO purchase_contract (date, place, no_of_installments, interest_rate, person, house)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        execute_query(self.db, query, tuple(data.values()))
        print("\nPurchase contract created successfully.")

    def list_contracts(self):
        print("\n--- List Contracts ---")
        print("1. List Tenancy Contracts")
        print("2. List Purchase Contracts")
        print("3. Back")
        choice = input("Choose an option: ")

        match choice:
            case "1":
                query = """
                    SELECT contract_id, date, place, start_date, duration, additional_costs, person, apartment
                    FROM tenancy_contract
                """
            case "2":
                query = """
                    SELECT contract_id, date, place, no_of_installments, interest_rate, person, house
                    FROM purchase_contract
                """
            case "3":
                return
            case _:
                print("Invalid choice.")
                return

        results = execute_query(self.db, query, fetch=True)
        if not results:
            print("No contracts found.")
        else:
            for row in results:
                print(row)
