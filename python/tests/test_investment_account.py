import unittest
from src.person import Person
from src.business import Business
from src.investment_account import InvestmentAccount


# All monetary values are integers representing cents.
# e.g. 100000 cents = $1,000.00


class TestInvestmentAccount(unittest.TestCase):

    def test_constructor_with_person(self):
        # Given
        account_holder = Person("John", "Doe", "john@example.com", "555-1234")
        balance = 1000000  # $10,000.00 in cents
        account_number = "INV001"
        interest_rate = 0.07  # 7%

        # When
        account = InvestmentAccount(account_holder, balance, account_number, interest_rate)

        # Then
        self.assertIsNotNone(account)
        self.assertEqual(account_holder, account.get_account_holder())
        self.assertEqual(balance, account.get_balance())
        self.assertEqual(account_number, account.get_account_number())

    def test_constructor_with_business(self):
        # Given
        account_holder = Business("Global Industries")
        balance = 5000000  # $50,000.00 in cents
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
        account = InvestmentAccount(account_holder, 1500000, "INV003", expected_interest_rate)

        # When
        actual_interest_rate = account.get_interest_rate()

        # Then
        self.assertAlmostEqual(expected_interest_rate, actual_interest_rate, places=4)

    def test_set_interest_rate(self):
        # Given
        account_holder = Person("Bob", "Jones", "bob@example.com", "555-9999")
        account = InvestmentAccount(account_holder, 2000000, "INV004", 0.05)
        new_interest_rate = 0.09

        # When
        account.set_interest_rate(new_interest_rate)

        # Then
        self.assertAlmostEqual(new_interest_rate, account.get_interest_rate(), places=4)

    def test_apply_interest(self):
        # Given
        account_holder = Person("Alice", "Brown", "alice@example.com", "555-1111")
        initial_balance = 1000000  # $10,000.00 in cents
        interest_rate = 0.10  # 10%
        account = InvestmentAccount(account_holder, initial_balance, "INV005", interest_rate)

        # When
        account.apply_interest()

        # Then
        expected_balance = 1100000  # $11,000.00 in cents
        self.assertEqual(expected_balance, account.get_balance())

    def test_multiple_interest_applications(self):
        # Given
        account_holder = Person("Charlie", "Wilson", "charlie@example.com", "555-2222")
        initial_balance = 500000  # $5,000.00 in cents
        interest_rate = 0.05  # 5%
        account = InvestmentAccount(account_holder, initial_balance, "INV006", interest_rate)

        # When
        account.apply_interest()  # 500000 * 1.05 = 525000
        account.apply_interest()  # 525000 * 1.05 = 551250

        # Then
        expected_balance = 551250  # $5,512.50 in cents
        self.assertEqual(expected_balance, account.get_balance())

    def test_investment_account_allows_overdraft(self):
        # Given
        account_holder = Person("David", "Miller", "david@example.com", "555-3333")
        account = InvestmentAccount(account_holder, 100000, "INV007", 0.07)  # $1,000.00

        # When - Attempting to overdraw (no overdraft protection)
        account.debit(150000)  # $1,500.00

        # Then - Balance goes negative
        self.assertEqual(-50000, account.get_balance())  # -$500.00

    def test_debit_with_sufficient_funds(self):
        # Given
        account_holder = Person("Eve", "Davis", "eve@example.com", "555-4444")
        account = InvestmentAccount(account_holder, 800000, "INV008", 0.06)  # $8,000.00

        # When
        account.debit(300000)  # $3,000.00

        # Then
        self.assertEqual(500000, account.get_balance())  # $5,000.00

    def test_credit_in_investment_account(self):
        # Given
        account_holder = Person("Frank", "Garcia", "frank@example.com", "555-5555")
        account = InvestmentAccount(account_holder, 1200000, "INV009", 0.08)  # $12,000.00

        # When
        account.credit(300000)  # $3,000.00

        # Then
        self.assertEqual(1500000, account.get_balance())  # $15,000.00

    def test_high_interest_rate(self):
        # Given
        account_holder = Person("Grace", "Martinez", "grace@example.com", "555-6666")
        initial_balance = 10000000  # $100,000.00 in cents
        interest_rate = 0.15  # 15%
        account = InvestmentAccount(account_holder, initial_balance, "INV010", interest_rate)

        # When
        account.apply_interest()

        # Then
        expected_balance = 11500000  # $115,000.00 in cents
        self.assertEqual(expected_balance, account.get_balance())

    def test_transactions_and_interest(self):
        # Given
        account_holder = Person("Henry", "Rodriguez", "henry@example.com", "555-7777")
        account = InvestmentAccount(account_holder, 1000000, "INV011", 0.10)  # $10,000.00

        # When
        account.credit(500000)      # +$5,000.00  -> 1500000
        account.apply_interest()    # 1500000 * 1.10 = 1650000
        account.debit(650000)       # -$6,500.00  -> 1000000

        # Then
        self.assertEqual(1000000, account.get_balance())  # $10,000.00


if __name__ == "__main__":
    unittest.main()

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
