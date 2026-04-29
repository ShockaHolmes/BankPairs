import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.person import Person
from src.business import Business
from src.checking_account import CheckingAccount


class TestCheckingAccount(unittest.TestCase):

    def test_constructor_with_person(self):
        # Given
        account_holder = Person("John", "Doe", "john@example.com", "555-1234")
        balance = 1000.0
        account_number = "CHK001"
        overdraft_protection = True

        # When
        account = CheckingAccount(account_holder, balance, account_number, overdraft_protection)

        # Then
        self.assertIsNotNone(account)
        self.assertEqual(account_holder, account.get_account_holder())
        self.assertAlmostEqual(balance, account.get_balance(), places=2)
        self.assertEqual(account_number, account.get_account_number())

    def test_constructor_with_business(self):
        # Given
        account_holder = Business("Acme Corp")
        balance = 5000.0
        account_number = "CHK002"
        overdraft_protection = False

        # When
        account = CheckingAccount(account_holder, balance, account_number, overdraft_protection)

        # Then
        self.assertIsNotNone(account)
        self.assertEqual(account_holder, account.get_account_holder())

    def test_get_overdraft_protection(self):
        # Given
        account_holder = Person("Jane", "Smith", "jane@example.com", "555-5678")
        expected_overdraft_protection = True
        account = CheckingAccount(account_holder, 1000.0, "CHK003", expected_overdraft_protection)

        # When
        actual_overdraft_protection = account.get_overdraft_protection()

        # Then
        self.assertEqual(expected_overdraft_protection, actual_overdraft_protection)

    def test_set_overdraft_protection(self):
        # Given
        account_holder = Person("Bob", "Jones", "bob@example.com", "555-9999")
        account = CheckingAccount(account_holder, 1000.0, "CHK004", True)

        # When
        account.set_overdraft_protection(False)

        # Then
        self.assertFalse(account.get_overdraft_protection())

    def test_debit_with_overdraft_protection_enabled(self):
        # Given
        account_holder = Person("Alice", "Brown", "alice@example.com", "555-1111")
        account = CheckingAccount(account_holder, 500.0, "CHK005", True)

        # When - Attempting to overdraw
        account.debit(600.0)

        # Then - Balance should remain unchanged because overdraft protection is enabled
        self.assertAlmostEqual(500.0, account.get_balance(), places=2)

    def test_debit_with_overdraft_protection_disabled(self):
        # Given
        account_holder = Person("Charlie", "Wilson", "charlie@example.com", "555-2222")
        account = CheckingAccount(account_holder, 500.0, "CHK006", False)

        # When - Attempting to overdraw
        account.debit(600.0)

        # Then - Balance should go negative because overdraft protection is disabled
        self.assertAlmostEqual(-100.0, account.get_balance(), places=2)

    def test_debit_with_sufficient_funds(self):
        # Given
        account_holder = Person("David", "Miller", "david@example.com", "555-3333")
        account = CheckingAccount(account_holder, 1000.0, "CHK007", True)

        # When
        account.debit(300.0)

        # Then
        self.assertAlmostEqual(700.0, account.get_balance(), places=2)

    def test_credit_in_checking_account(self):
        # Given
        account_holder = Person("Eve", "Davis", "eve@example.com", "555-4444")
        account = CheckingAccount(account_holder, 1000.0, "CHK008", True)

        # When
        account.credit(500.0)

        # Then
        self.assertAlmostEqual(1500.0, account.get_balance(), places=2)

    def test_multiple_transactions(self):
        # Given
        account_holder = Person("Frank", "Garcia", "frank@example.com", "555-5555")
        account = CheckingAccount(account_holder, 1000.0, "CHK009", False)

        # When
        account.credit(200.0)
        account.debit(300.0)
        account.credit(100.0)

        # Then
        self.assertAlmostEqual(1000.0, account.get_balance(), places=2)


if __name__ == "__main__":
    unittest.main()
