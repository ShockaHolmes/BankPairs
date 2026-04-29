import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.bank_system import BankSystem
from src.checking_account import CheckingAccount
from src.person import Person


class TestBankSystem(unittest.TestCase):

    def test_customer_log_has_labeled_columns(self):
        bank_system = BankSystem()
        customer = Person("Jane", "Doe", "jane@example.com", "555-0000")
        account = CheckingAccount(customer, 1000.0, "CHK100", True)
        bank_system.add_account(account)

        customer_log = bank_system.get_customer_log()

        self.assertIn("Customer Name", customer_log)
        self.assertIn("Account Type", customer_log)
        self.assertIn("Email", customer_log)
        self.assertIn("Phone Number", customer_log)

    def test_lookup_customer_by_email(self):
        bank_system = BankSystem()
        customer = Person("Jane", "Doe", "jane@example.com", "555-0000")
        account = CheckingAccount(customer, 1000.0, "CHK101", True)
        bank_system.add_account(account)

        matches = bank_system.lookup_customer("jane@example.com")

        self.assertEqual(1, len(matches))
        self.assertEqual("Jane Doe", matches[0]["customer_name"])

    def test_deposit_and_withdraw_update_transaction_history(self):
        bank_system = BankSystem()
        customer = Person("Jane", "Doe", "jane@example.com", "555-0000")
        account = CheckingAccount(customer, 1000.0, "CHK102", False)
        bank_system.add_account(account)

        bank_system.deposit_to_account("CHK102", 250.0)
        bank_system.withdraw_from_account("CHK102", 100.0)

        transactions = bank_system.get_customer_transactions("CHK102")

        self.assertEqual(2, len(transactions))
        self.assertIn("Credited: 250.00", transactions[0])
        self.assertIn("Debited: 100.00", transactions[1])


if __name__ == "__main__":
    unittest.main()