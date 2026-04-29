import unittest
import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.person import Person
from src.checking_account import CheckingAccount


class TestAccount(unittest.TestCase):

    # Helper method to create a concrete account for testing.
    # Since Account is abstract, we need a concrete implementation for testing.
    def create_test_account(self, account_holder, balance, account_number):
        return CheckingAccount(account_holder, balance, account_number, True)

    def test_get_account_holder(self):
        # Given
        account_holder = Person("John", "Doe", "john@example.com", "555-1234")
        account = self.create_test_account(account_holder, 1000.0, "ACC001")

        # When
        actual_holder = account.get_account_holder()

        # Then
        self.assertEqual(account_holder, actual_holder)

    def test_get_balance(self):
        # Given
        account_holder = Person("Jane", "Smith", "jane@example.com", "555-5678")
        expected_balance = 1500.0
        account = self.create_test_account(account_holder, expected_balance, "ACC002")

        # When
        actual_balance = account.get_balance()

        # Then
        self.assertAlmostEqual(expected_balance, actual_balance, places=2)

    def test_get_account_number(self):
        # Given
        account_holder = Person("Bob", "Jones", "bob@example.com", "555-9999")
        expected_account_number = "ACC003"
        account = self.create_test_account(account_holder, 500.0, expected_account_number)

        # When
        actual_account_number = account.get_account_number()

        # Then
        self.assertEqual(expected_account_number, actual_account_number)

    def test_credit(self):
        # Given
        account_holder = Person("Alice", "Brown", "alice@example.com", "555-1111")
        account = self.create_test_account(account_holder, 1000.0, "ACC004")
        credit_amount = 500.0

        # When
        account.credit(credit_amount)

        # Then
        expected_balance = 1500.0
        self.assertAlmostEqual(expected_balance, account.get_balance(), places=2)

    def test_debit(self):
        # Given
        account_holder = Person("Charlie", "Wilson", "charlie@example.com", "555-2222")
        account = self.create_test_account(account_holder, 1000.0, "ACC005")
        debit_amount = 300.0

        # When
        account.debit(debit_amount)

        # Then
        expected_balance = 700.0
        self.assertAlmostEqual(expected_balance, account.get_balance(), places=2)

    def test_get_transactions(self):
        # Given
        account_holder = Person("David", "Miller", "david@example.com", "555-3333")
        account = self.create_test_account(account_holder, 1000.0, "ACC006")

        # When
        account.credit(200.0)
        account.debit(100.0)
        transactions = account.get_transactions()

        # Then
        self.assertIsNotNone(transactions)

    def test_transaction_recording_after_credit(self):
        # Given
        account_holder = Person("Eve", "Davis", "eve@example.com", "555-4444")
        account = self.create_test_account(account_holder, 1000.0, "ACC007")

        # When
        account.credit(250.0)
        transactions = account.get_transactions()

        # Then
        self.assertIsNotNone(transactions)
        # Students should implement a way to verify that the transaction was recorded

    def test_transaction_recording_after_debit(self):
        # Given
        account_holder = Person("Frank", "Garcia", "frank@example.com", "555-5555")
        account = self.create_test_account(account_holder, 1000.0, "ACC008")

        # When
        account.debit(150.0)
        transactions = account.get_transactions()

        # Then
        self.assertIsNotNone(transactions)
        # Students should implement a way to verify that the transaction was recorded

    def test_set_balance(self):
        # Given
        account_holder = Person("Grace", "Martinez", "grace@example.com", "555-6666")
        account = self.create_test_account(account_holder, 1000.0, "ACC009")
        new_balance = 2000.0

        # When
        account.set_balance(new_balance)

        # Then
        self.assertAlmostEqual(new_balance, account.get_balance(), places=2)


if __name__ == "__main__":
    unittest.main()
