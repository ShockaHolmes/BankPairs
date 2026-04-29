import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.person import Person
from src.business import Business
from src.savings_account import SavingsAccount


class TestSavingsAccount(unittest.TestCase):

    def test_constructor_with_person(self):
        # Given
        account_holder = Person("John", "Doe", "john@example.com", "555-1234")
        balance = 2000.0
        account_number = "SAV001"
        interest_rate = 0.02  # 2% interest rate

        # When
        account = SavingsAccount(account_holder, balance, account_number, interest_rate)

        # Then
        self.assertIsNotNone(account)
        self.assertEqual(account_holder, account.get_account_holder())
        self.assertAlmostEqual(balance, account.get_balance(), places=2)
        self.assertEqual(account_number, account.get_account_number())

    def test_constructor_with_business(self):
        # Given
        account_holder = Business("Tech Solutions Inc")
        balance = 10000.0
        account_number = "SAV002"
        interest_rate = 0.03

        # When
        account = SavingsAccount(account_holder, balance, account_number, interest_rate)

        # Then
        self.assertIsNotNone(account)
        self.assertEqual(account_holder, account.get_account_holder())

    def test_get_interest_rate(self):
        # Given
        account_holder = Person("Jane", "Smith", "jane@example.com", "555-5678")
        expected_interest_rate = 0.025
        account = SavingsAccount(account_holder, 5000.0, "SAV003", expected_interest_rate)

        # When
        actual_interest_rate = account.get_interest_rate()

        # Then
        self.assertAlmostEqual(expected_interest_rate, actual_interest_rate, places=4)

    def test_set_interest_rate(self):
        # Given
        account_holder = Person("Bob", "Jones", "bob@example.com", "555-9999")
        account = SavingsAccount(account_holder, 3000.0, "SAV004", 0.02)
        new_interest_rate = 0.03

        # When
        account.set_interest_rate(new_interest_rate)

        # Then
        self.assertAlmostEqual(new_interest_rate, account.get_interest_rate(), places=4)

    def test_apply_interest(self):
        # Given
        account_holder = Person("Alice", "Brown", "alice@example.com", "555-1111")
        initial_balance = 1000.0
        interest_rate = 0.05  # 5%
        account = SavingsAccount(account_holder, initial_balance, "SAV005", interest_rate)

        # When
        account.apply_interest()

        # Then
        expected_balance = 1050.0  # 1000 + (1000 * 0.05)
        self.assertAlmostEqual(expected_balance, account.get_balance(), places=2)

    def test_multiple_interest_applications(self):
        # Given
        account_holder = Person("Charlie", "Wilson", "charlie@example.com", "555-2222")
        initial_balance = 1000.0
        interest_rate = 0.10  # 10%
        account = SavingsAccount(account_holder, initial_balance, "SAV006", interest_rate)

        # When
        account.apply_interest()
        account.apply_interest()

        # Then
        expected_balance = 1210.0  # 1000 * 1.1 * 1.1
        self.assertAlmostEqual(expected_balance, account.get_balance(), places=2)

    def test_savings_account_has_overdraft_protection(self):
        # Given
        account_holder = Person("David", "Miller", "david@example.com", "555-3333")
        account = SavingsAccount(account_holder, 500.0, "SAV007", 0.02)

        # When - Attempting to overdraw
        account.debit(600.0)

        # Then - Balance should remain unchanged because savings accounts have overdraft protection
        self.assertAlmostEqual(500.0, account.get_balance(), places=2)

    def test_debit_with_sufficient_funds(self):
        # Given
        account_holder = Person("Eve", "Davis", "eve@example.com", "555-4444")
        account = SavingsAccount(account_holder, 1000.0, "SAV008", 0.03)

        # When
        account.debit(300.0)

        # Then
        self.assertAlmostEqual(700.0, account.get_balance(), places=2)

    def test_credit_in_savings_account(self):
        # Given
        account_holder = Person("Frank", "Garcia", "frank@example.com", "555-5555")
        account = SavingsAccount(account_holder, 2000.0, "SAV009", 0.025)

        # When
        account.credit(500.0)

        # Then
        self.assertAlmostEqual(2500.0, account.get_balance(), places=2)

    def test_interest_on_zero_balance(self):
        # Given
        account_holder = Person("Grace", "Martinez", "grace@example.com", "555-6666")
        account = SavingsAccount(account_holder, 0.0, "SAV010", 0.05)

        # When
        account.apply_interest()

        # Then
        self.assertAlmostEqual(0.0, account.get_balance(), places=2)

    def test_transactions_and_interest(self):
        # Given
        account_holder = Person("Henry", "Rodriguez", "henry@example.com", "555-7777")
        account = SavingsAccount(account_holder, 1000.0, "SAV011", 0.05)

        # When
        account.credit(500.0)       # Balance: 1500
        account.apply_interest()    # Balance: 1575 (1500 * 1.05)
        account.debit(575.0)        # Balance: 1000

        # Then
        self.assertAlmostEqual(1000.0, account.get_balance(), places=2)


if __name__ == "__main__":
    unittest.main()
