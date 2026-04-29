import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.person import Person
from src.business import Business
from src.investment_account import InvestmentAccount


class TestInvestmentAccount(unittest.TestCase):

    def test_constructor_with_person(self):
        # Given
        account_holder = Person("John", "Doe", "john@example.com", "555-1234")
        balance = 10000.0
        account_number = "INV001"
        interest_rate = 0.07  # 7% interest rate

        # When
        account = InvestmentAccount(account_holder, balance, account_number, interest_rate)

        # Then
        self.assertIsNotNone(account)
        self.assertEqual(account_holder, account.get_account_holder())
        self.assertAlmostEqual(balance, account.get_balance(), places=2)
        self.assertEqual(account_number, account.get_account_number())

    def test_constructor_with_business(self):
        # Given
        account_holder = Business("Global Industries")
        balance = 50000.0
        account_number = "INV002"
        interest_rate = 0.08

        # When
        account = InvestmentAccount(account_holder, balance, account_number, interest_rate)

        # Then
        self.assertIsNotNone(account)
        self.assertEqual(account_holder, account.get_account_holder())

    def test_get_interest_rate(self):
        # Given
        account_holder = Person("Jane", "Smith", "jane@example.com", "555-5678")
        expected_interest_rate = 0.06
        account = InvestmentAccount(account_holder, 15000.0, "INV003", expected_interest_rate)

        # When
        actual_interest_rate = account.get_interest_rate()

        # Then
        self.assertAlmostEqual(expected_interest_rate, actual_interest_rate, places=4)

    def test_set_interest_rate(self):
        # Given
        account_holder = Person("Bob", "Jones", "bob@example.com", "555-9999")
        account = InvestmentAccount(account_holder, 20000.0, "INV004", 0.05)
        new_interest_rate = 0.09

        # When
        account.set_interest_rate(new_interest_rate)

        # Then
        self.assertAlmostEqual(new_interest_rate, account.get_interest_rate(), places=4)

    def test_apply_interest(self):
        # Given
        account_holder = Person("Alice", "Brown", "alice@example.com", "555-1111")
        initial_balance = 10000.0
        interest_rate = 0.10  # 10%
        account = InvestmentAccount(account_holder, initial_balance, "INV005", interest_rate)

        # When
        account.apply_interest()

        # Then
        expected_balance = 11000.0  # 10000 + (10000 * 0.10)
        self.assertAlmostEqual(expected_balance, account.get_balance(), places=2)

    def test_multiple_interest_applications(self):
        # Given
        account_holder = Person("Charlie", "Wilson", "charlie@example.com", "555-2222")
        initial_balance = 5000.0
        interest_rate = 0.05  # 5%
        account = InvestmentAccount(account_holder, initial_balance, "INV006", interest_rate)

        # When
        account.apply_interest()
        account.apply_interest()

        # Then
        expected_balance = 5512.50  # 5000 * 1.05 * 1.05
        self.assertAlmostEqual(expected_balance, account.get_balance(), places=2)

    def test_investment_account_allows_overdraft(self):
        # Given
        account_holder = Person("David", "Miller", "david@example.com", "555-3333")
        account = InvestmentAccount(account_holder, 1000.0, "INV007", 0.07)

        # When - Attempting to overdraw (investment accounts don't have overdraft protection)
        account.debit(1500.0)

        # Then - Balance should go negative
        self.assertAlmostEqual(-500.0, account.get_balance(), places=2)

    def test_debit_with_sufficient_funds(self):
        # Given
        account_holder = Person("Eve", "Davis", "eve@example.com", "555-4444")
        account = InvestmentAccount(account_holder, 8000.0, "INV008", 0.06)

        # When
        account.debit(3000.0)

        # Then
        self.assertAlmostEqual(5000.0, account.get_balance(), places=2)

    def test_credit_in_investment_account(self):
        # Given
        account_holder = Person("Frank", "Garcia", "frank@example.com", "555-5555")
        account = InvestmentAccount(account_holder, 12000.0, "INV009", 0.08)

        # When
        account.credit(3000.0)

        # Then
        self.assertAlmostEqual(15000.0, account.get_balance(), places=2)

    def test_high_interest_rate(self):
        # Given
        account_holder = Person("Grace", "Martinez", "grace@example.com", "555-6666")
        initial_balance = 100000.0
        interest_rate = 0.15  # 15% - Higher than savings account
        account = InvestmentAccount(account_holder, initial_balance, "INV010", interest_rate)

        # When
        account.apply_interest()

        # Then
        expected_balance = 115000.0
        self.assertAlmostEqual(expected_balance, account.get_balance(), places=2)

    def test_transactions_and_interest(self):
        # Given
        account_holder = Person("Henry", "Rodriguez", "henry@example.com", "555-7777")
        account = InvestmentAccount(account_holder, 10000.0, "INV011", 0.10)

        # When
        account.credit(5000.0)      # Balance: 15000
        account.apply_interest()    # Balance: 16500 (15000 * 1.10)
        account.debit(6500.0)       # Balance: 10000

        # Then
        self.assertAlmostEqual(10000.0, account.get_balance(), places=2)

    def test_interest_on_negative_balance(self):
        # Given
        account_holder = Person("Ivy", "Lee", "ivy@example.com", "555-8888")
        account = InvestmentAccount(account_holder, -1000.0, "INV012", 0.10)

        # When
        account.apply_interest()

        # Then
        # Interest on negative balance: -1000 + (-1000 * 0.10) = -1100
        self.assertAlmostEqual(-1100.0, account.get_balance(), places=2)


if __name__ == "__main__":
    unittest.main()
