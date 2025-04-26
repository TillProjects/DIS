from db_connection_manager import db_connection_manager

class ContractManager:
    def __init__(self):
        self.db = db_connection_manager.get_instance().get_connection()

    def contract_menu(self):
        while True:
            print("\n--- Contract Management ---")
            print("1. Create Tenancy Contract (Apartment)")
            print("2. Create Purchase Contract (House)")
            print("3. List Contracts")
            print("4. Back")
            choice = input("Choose an option: ")

            if choice == "1":
                self.create_tenancy_contract()
            elif choice == "2":
                self.create_purchase_contract()
            elif choice == "3":
                self.list_contracts()
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")


    def create_tenancy_contract(self):
        print("\n--- Create Tenancy Contract ---")
        date = input("Contract Date (YYYY-MM-DD): ")
        place = input("Place: ")
        start_date = input("Start Date (YYYY-MM-DD): ")
        duration = input("Duration (months): ")
        additional_costs = input("Additional Costs: ")
        person_id = input("Person ID: ")
        apartment_id = input("Apartment ID: ")

        cur = self.db.cursor()
        try:
            cur.execute(
                """
                INSERT INTO tenancy_contract (date, place, start_date, duration, additional_costs, person, apartment)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (date, place, start_date, duration, additional_costs, person_id, apartment_id)
            )
            self.db.commit()
            print("\nTenancy contract created successfully.")
        except Exception as e:
            print(f"\nError creating tenancy contract: {e}")
            self.db.rollback()
        finally:
            cur.close()

    def create_purchase_contract(self):
        print("\n--- Create Purchase Contract ---")
        date = input("Contract Date (YYYY-MM-DD): ")
        place = input("Place: ")
        no_of_installments = input("Number of Installments: ")
        interest_rate = input("Interest Rate (%): ")
        person_id = input("Person ID: ")
        house_id = input("House ID: ")

        cur = self.db.cursor()
        try:
            cur.execute(
                """
                INSERT INTO purchase_contract (date, place, no_of_installments, interest_rate, person, house)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (date, place, no_of_installments, interest_rate, person_id, house_id)
            )
            self.db.commit()
            print("\nPurchase contract created successfully.")
        except Exception as e:
            print(f"\nError creating purchase contract: {e}")
            self.db.rollback()
        finally:
            cur.close()

    def list_contracts(self):
        print("\n--- List Contracts ---")
        print("1. List Tenancy Contracts")
        print("2. List Purchase Contracts")
        print("3. Back")
        choice = input("Choose an option: ")
    
        cur = self.db.cursor()
        try:
            if choice == "1":
                cur.execute(
                    """
                    SELECT contract_id, date, place, start_date, duration, additional_costs, person, apartment
                    FROM tenancy_contract
                """
                )
                contracts = cur.fetchall()
                if not contracts:
                    print("No tenancy contracts found.")
                else:
                    for contract in contracts:
                        print(contract)
            elif choice == "2":
                cur.execute(
                    """
                    SELECT contract_id, date, place, no_of_installments, interest_rate, person, house
                    FROM purchase_contract
                """
                )
                contracts = cur.fetchall()
                if not contracts:
                    print("No purchase contracts found.")
                else:
                    for contract in contracts:
                        print(contract)
            elif choice == "3":
                return
            else:
                print("Invalid choice.")
        except Exception as e:
            print(f"\nError listing contracts: {e}")
        finally:
            cur.close()
