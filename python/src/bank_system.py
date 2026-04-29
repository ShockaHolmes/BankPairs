import json
import os
from pathlib import Path
from src.business import Business
from src.checking_account import CheckingAccount
from src.investment_account import InvestmentAccount
from src.person import Person
from src.savings_account import SavingsAccount


class BankSystem:
    def __init__(self):
        self._accounts = []
        self._data_file = Path("bank_data.json")
        self._account_counter = {"CHK": 1000, "SAV": 2000, "INV": 3000}
        self._default_interest_rates = {"savings": 0.02, "investment": 0.05}
        self.load_accounts()

    def add_account(self, account):
        self._accounts.append(account)
        return account

    def get_accounts(self):
        return self._accounts

    def find_account(self, account_number):
        for account in self._accounts:
            if account.get_account_number() == account_number:
                return account
        return None

    def deposit_to_account(self, account_number, amount):
        account = self.find_account(account_number)
        if account is None:
            return None

        account.deposit(amount)
        return account.get_account_summary()

    def withdraw_from_account(self, account_number, amount):
        account = self.find_account(account_number)
        if account is None:
            return None

        account.withdraw(amount)
        return account.get_account_summary()

    def apply_interest_to_account(self, account_number):
        account = self.find_account(account_number)
        if account is None or not hasattr(account, "apply_interest"):
            return None

        account.apply_interest()
        return account.get_account_summary()

    def lookup_customer(self, search_value):
        matches = []
        search_value = search_value.lower()

        for account in self._accounts:
            summary = account.get_account_summary()
            searchable_values = [
                summary["customer_name"],
                summary["account_number"],
                summary["email"],
                summary["phone_number"],
            ]
            if any(search_value in str(value).lower() for value in searchable_values):
                matches.append(summary)

        return matches

    def get_customer_log(self):
        columns = [
            ("Customer Name", 20),
            ("Account Type", 18),
            ("Account Number", 16),
            ("Balance", 12),
            ("Email", 28),
            ("Phone Number", 16),
            ("Transactions", 45),
        ]

        if not self._accounts:
            return "No customer accounts available."

        header = " | ".join(title.ljust(width) for title, width in columns)
        divider = "-" * len(header)
        rows = [header, divider]

        for account in self._accounts:
            summary = account.get_account_summary()
            transaction_text = "; ".join(summary["transactions"])
            values = [
                summary["customer_name"],
                summary["account_type"],
                summary["account_number"],
                summary["balance"],
                summary["email"],
                summary["phone_number"],
                transaction_text,
            ]
            rows.append(
                " | ".join(
                    self._truncate(value, width).ljust(width)
                    for value, (_, width) in zip(values, columns)
                )
            )

        return "\n".join(rows)

    def get_customer_transactions(self, account_number):
        account = self.find_account(account_number)
        if account is None:
            return []
        return account.get_transactions()

    def display_menu(self):
        return (
            "\nWelcome to the Bank. Choose your option.\n"
            "Bank Menu\n"
            "1. Create checking account\n"
            "2. Create savings account\n"
            "3. Create investment account\n"
            "4. Deposit\n"
            "5. Withdraw\n"
            "6. Apply interest\n"
            "7. Show customer log\n"
            "8. Look up customer\n"
            "9. View transaction history\n"
            "10. View saved transactions from previous sessions\n"
            "0. Exit\n"
        )

    def run(self):
        while True:
            try:
                print(self.display_menu())
                choice = self._prompt_menu_choice()
            except (EOFError, KeyboardInterrupt):
                print("\nInput cancelled. Exiting bank system.")
                break

            try:
                if choice == "1":
                    account = self._create_account("checking")
                    self.add_account(account)
                    print("Checking account created.")
                elif choice == "2":
                    account = self._create_account("savings")
                    self.add_account(account)
                    print("Savings account created.")
                elif choice == "3":
                    account = self._create_account("investment")
                    self.add_account(account)
                    print("Investment account created.")
                elif choice == "4":
                    self._handle_deposit()
                elif choice == "5":
                    self._handle_withdraw()
                elif choice == "6":
                    self._handle_apply_interest()
                elif choice == "7":
                    print(self.get_customer_log())
                elif choice == "8":
                    self._handle_lookup()
                elif choice == "9":
                    self._handle_transactions()
                elif choice == "10":
                    self._handle_view_saved_transactions()
                elif choice == "0":
                    if self._prompt_confirmation("Are you sure you want to exit? (yes/no): "):
                        self.save_accounts()
                        print("Accounts saved. Goodbye.")
                        break
                    print("Exit cancelled.")
            except (EOFError, KeyboardInterrupt):
                print("\nInput cancelled. Returning to the main menu.")
            except Exception as error:
                print(f"An error occurred: {error}")
                print("Please try again.")

    def _create_account(self, account_type):
        account_holder = self._create_account_holder()
        balance = self._prompt_amount("Enter starting balance: ", allow_negative=False)
        account_number = self._generate_account_number(account_type)
        print(f"Auto-generated account number: {account_number}")

        if account_type == "checking":
            overdraft_protection = self._prompt_boolean(
                "Enable overdraft protection? (true/false): "
            )
            return CheckingAccount(account_holder, balance, account_number, overdraft_protection)

        interest_rate = self._get_default_interest_rate(account_type)
        print(f"Auto-assigned interest rate: {interest_rate * 100}%")
        if account_type == "savings":
            return SavingsAccount(account_holder, balance, account_number, interest_rate)

        return InvestmentAccount(account_holder, balance, account_number, interest_rate)

    def _create_account_holder(self):
        holder_type = self._prompt_choice(
            "Create a person or business account holder? (person/business): ",
            ["person", "business"],
        )

        if holder_type == "business":
            business_name = self._prompt_required_text("Enter business name: ")
            email = self._prompt_email("Enter business email: ")
            phone_number = self._prompt_phone_number("Enter business phone number: ")
            return Business(business_name, email, phone_number)

        first_name = self._prompt_required_text("Enter first name: ")
        last_name = self._prompt_required_text("Enter last name: ")
        dob = self._prompt_dob("Enter date of birth (dd/mm/yyyy): ")
        email = self._prompt_email("Enter email: ")
        phone_number = self._prompt_phone_number("Enter phone number: ")
        return Person(first_name, last_name, email, phone_number, dob)

    def _handle_deposit(self):
        account_number = self._prompt_required_text("Enter account number: ")
        amount = self._prompt_amount("Enter deposit amount: ", allow_negative=False)
        summary = self.deposit_to_account(account_number, amount)
        if summary is None:
            print("Account not found.")
            return
        print(f"Deposit complete. New balance: {summary['balance']}")

    def _handle_withdraw(self):
        account_number = self._prompt_required_text("Enter account number: ")
        amount = self._prompt_amount("Enter withdrawal amount: ", allow_negative=False)

        if not self._prompt_confirmation(
            "Are you sure you want to continue with this withdrawal? (yes/no): "
        ):
            print("Withdrawal cancelled.")
            return

        summary = self.withdraw_from_account(account_number, amount)
        if summary is None:
            print("Account not found.")
            return
        print(f"Withdrawal complete. New balance: {summary['balance']}")

    def _handle_apply_interest(self):
        account_number = self._prompt_required_text("Enter account number: ")
        summary = self.apply_interest_to_account(account_number)
        if summary is None:
            print("Account not found or interest is not available for this account.")
            return
        print(f"Interest applied. New balance: {summary['balance']}")

    def _handle_lookup(self):
        search_value = self._prompt_required_text(
            "Enter customer name, account number, email, or phone number: "
        )
        matches = self.lookup_customer(search_value)
        if not matches:
            print("No customer found.")
            return

        for match in matches:
            print(match)

    def _handle_transactions(self):
        account_number = self._prompt_required_text("Enter account number: ")
        transactions = self.get_customer_transactions(account_number)
        if not transactions:
            print("No transactions found.")
            return

        for transaction in transactions:
            print(transaction)

    def _truncate(self, value, width):
        value = str(value)
        if len(value) <= width:
            return value
        if width <= 3:
            return value[:width]
        return value[: width - 3] + "..."

    def _prompt_required_text(self, prompt):
        while True:
            value = self._read_input(prompt).strip()
            if value:
                return value
            print("Input cannot be blank. Please try again.")

    def _prompt_amount(self, prompt, allow_negative=True):
        while True:
            raw_value = self._read_input(prompt).strip()
            try:
                amount = float(raw_value)
                if not allow_negative and amount < 0:
                    print("Please enter 0 or a positive number.")
                    continue
                return amount
            except ValueError:
                print("Please enter a valid number.")

    def _prompt_boolean(self, prompt):
        return self._prompt_choice(prompt, ["true", "false", "yes", "no"]) in ["true", "yes"]

    def _prompt_choice(self, prompt, valid_choices):
        valid_lookup = {choice.lower(): choice.lower() for choice in valid_choices}

        while True:
            value = self._read_input(prompt).strip().lower()
            if value in valid_lookup:
                return valid_lookup[value]
            print(f"Invalid choice. Please enter one of: {', '.join(valid_choices)}")

    def _prompt_menu_choice(self):
        return self._prompt_choice(
            "Choose your option: ",
            ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
        )

    def _prompt_email(self, prompt):
        while True:
            email = self._read_input(prompt).strip().lower()
            if self._is_valid_email(email):
                return email
            print("Please enter a valid email address.")

    def _prompt_phone_number(self, prompt):
        while True:
            phone_number = self._read_input(prompt).strip()
            normalized_phone_number = self._normalize_phone_number(phone_number)

            if normalized_phone_number is not None:
                return normalized_phone_number

            print("Please enter a valid phone number with at least 7 digits.")

    def _read_input(self, prompt):
        return input(prompt)

    def _prompt_account_number(self, account_type):
        required_prefixes = {
            "checking": "CHK",
            "savings": "SAV",
            "investment": "INV",
        }
        required_prefix = required_prefixes.get(account_type, "")

        while True:
            account_number = self._prompt_required_text("Enter account number: ")
            if required_prefix and not account_number.upper().startswith(required_prefix):
                print(
                    f"Account number must start with {required_prefix} for a {account_type} account."
                )
                continue
            if self.find_account(account_number) is not None:
                print("That account number already exists. Please enter a unique account number.")
                continue
            return account_number

    def _prompt_confirmation(self, prompt):
        return self._prompt_choice(prompt, ["yes", "no"]) == "yes"

    def _prompt_dob(self, prompt):
        while True:
            dob = self._read_input(prompt).strip()
            if self._is_valid_dob(dob):
                return dob
            print("Please enter a valid date of birth in dd/mm/yyyy format.")

    def _is_valid_dob(self, dob):
        if len(dob) != 10 or dob[2] != "/" or dob[5] != "/":
            return False

        try:
            day = int(dob[0:2])
            month = int(dob[3:5])
            year = int(dob[6:10])
            if 1 <= day <= 31 and 1 <= month <= 12 and year > 1900:
                return True
        except ValueError:
            pass
        return False

    def _generate_account_number(self, account_type):
        prefix_map = {"checking": "CHK", "savings": "SAV", "investment": "INV"}
        prefix = prefix_map.get(account_type, "ACC")
        account_number = f"{prefix}{self._account_counter[prefix]}"
        self._account_counter[prefix] += 1
        return account_number

    def _get_default_interest_rate(self, account_type):
        return self._default_interest_rates.get(account_type, 0.0)

    def save_accounts(self):
        data = []
        for account in self._accounts:
            summary = account.get_account_summary()
            account_data = {
                "account_number": account.get_account_number(),
                "account_type": account.get_account_type(),
                "customer_name": summary["customer_name"],
                "balance": account.get_balance(),
                "email": summary["email"],
                "phone_number": summary["phone_number"],
                "transactions": account.get_transactions(),
            }
            data.append(account_data)

        try:
            with open(self._data_file, "w") as file:
                json.dump(data, file, indent=2)
        except Exception as error:
            print(f"Failed to save account data: {error}")

    def load_accounts(self):
        if not self._data_file.exists():
            return

        try:
            with open(self._data_file, "r") as file:
                data = json.load(file)
                if data:
                    print(f"Loaded {len(data)} account(s) from saved data.")
        except Exception as error:
            print(f"Failed to load account data: {error}")

    def _handle_view_saved_transactions(self):
        if not self._data_file.exists():
            print("No saved transaction data found.")
            return

        try:
            with open(self._data_file, "r") as file:
                data = json.load(file)
                if not data:
                    print("No saved transactions found.")
                    return

                print("\nSaved Transactions from Previous Sessions:")
                print("-" * 100)
                for account_data in data:
                    print(f"Account: {account_data['account_number']} ({account_data['customer_name']})")
                    transactions = account_data.get("transactions", [])
                    if transactions:
                        for transaction in transactions:
                            print(f"  {transaction}")
                    else:
                        print("  No transactions recorded.")
                    print()
        except Exception as error:
            print(f"Failed to read saved transactions: {error}")


    def _is_valid_email(self, email):
        if email.count("@") != 1:
            return False

        local_part, domain = email.split("@")
        if not local_part or not domain or "." not in domain:
            return False

        top_level_domain = domain.rsplit(".", 1)[-1]
        return len(top_level_domain) >= 2

    def _normalize_phone_number(self, phone_number):
        digits_only = "".join(character for character in phone_number if character.isdigit())

        if len(digits_only) == 10:
            return f"({digits_only[:3]}) {digits_only[3:6]}-{digits_only[6:]}"

        if len(digits_only) == 11 and digits_only.startswith("1"):
            return f"+1 ({digits_only[1:4]}) {digits_only[4:7]}-{digits_only[7:]}"

        return None