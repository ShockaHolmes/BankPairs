import unittest
from src.person import Person
from src.business import Business
from src.savings_account import SavingsAccount


# All monetary values are integers representing cents.
# e.g. 100000 cents = $1,000.00


class TestSavingsAccount(unittest.TestCase):

    def test_constructor_with_person(self):
        # Given
        account_holder = Person("John", "Doe", "john@example.com", "555-1234")
        balance = 200000  # $2,000.00 in cents
        account_number = "SAV001"
        interest_rate = 0.02  # 2%

        # When
        account = SavingsAccount(account_holder, balance, account_number, interest_rate)

        # Then
        self.assertIsNotNone(account)
        self.assertEqual(account_holder, account.get_account_holder())
        self.assertEqual(balance, account.get_balance())
        self.assertEqual(account_number, account.get_account_number())

    def test_constructor_with_business(self):
        # Given
        account_holder = Business("Tech Solutions Inc")
        balance = 1000000  # $10,000.00 in cents
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
        account = SavingsAccount(account_holder, 500000, "SAV003", expected_interest_rate)

        # When
        actual_interest_rate = account.get_interest_rate()

        # Then
        self.assertAlmostEqual(expected_interest_rate, actual_interest_rate, places=4)

    def test_set_interest_rate(self):
        # Given
        account_holder = Person("Bob", "Jones", "bob@example.com", "555-9999")
        account = SavingsAccount(account_holder, 300000, "SAV004", 0.02)
        new_interest_rate = 0.03

        # When
        account.set_interest_rate(new_interest_rate)

        # Then
        self.assertAlmostEqual(new_interest_rate, account.get_interest_rate(), places=4)

    def test_apply_interest(self):
        # Given
        account_holder = Person("Alice", "Brown", "alice@example.com", "555-1111")
        initial_balance = 100000  # $1,000.00 in cents
        interest_rate = 0.05  # 5%
        account = SavingsAccount(account_holder, initial_balance, "SAV005", interest_rate)

        # When
        account.apply_interest()

        # Then
        expected_balance = 105000  # $1,050.00 in cents
        self.assertEqual(expected_balance, account.get_balance())

    def test_multiple_interest_applications(self):
        # Given
        account_holder = Person("Charlie", "Wilson", "charlie@example.com", "555-2222")
        initial_balance = 100000  # $1,000.00 in cents
        interest_rate = 0.10  # 10%
        account = SavingsAccount(account_holder, initial_balance, "SAV006", interest_rate)

        # When
        account.apply_interest()  # 100000 * 1.10 = 110000
        account.apply_interest()  # 110000 * 1.10 = 121000

        # Then
        expected_balance = 121000  # $1,210.00 in cents
        self.assertEqual(expected_balance, account.get_balance())

    def test_savings_account_has_overdraft_protection(self):
        # Given
        account_holder = Person("David", "Miller", "david@example.com", "555-3333")
        account = SavingsAccount(account_holder, 50000, "SAV007", 0.02)  # $500.00

        # When - Attempting to overdraw
        account.debit(60000)  # $600.00

        # Then - Balance should remain unchanged (overdraft protection)
        self.assertEqual(50000, account.get_balance())

    def test_debit_with_sufficient_funds(self):
        # Given
        account_holder = Person("Eve", "Davis", "eve@example.com", "555-4444")
        account = SavingsAccount(account_holder, 100000, "SAV008", 0.03)  # $1,000.00

        # When
        account.debit(30000)  # $300.00

        # Then
        self.assertEqual(70000, account.get_balance())  # $700.00

    def test_credit_in_savings_account(self):
        # Given
        account_holder = Person("Frank", "Garcia", "frank@example.com", "555-5555")
        account = SavingsAccount(account_holder, 200000, "SAV009", 0.025)  # $2,000.00

        # When
        account.credit(50000)  # $500.00

        # Then
        self.assertEqual(250000, account.get_balance())  # $2,500.00

    def test_interest_on_zero_balance(self):
        # Given
        account_holder = Person("Grace", "Martinez", "grace@example.com", "555-6666")
        account = SavingsAccount(account_holder, 0, "SAV010", 0.05)

        # When
        account.apply_interest()

        # Then
        self.assertEqual(0, account.get_balance())

    def test_transactions_and_interest(self):
        # Given
        account_holder = Person("Henry", "Rodriguez", "henry@example.com", "555-7777")
        account = SavingsAccount(account_holder, 100000, "SAV011", 0.05)  # $1,000.00

        # When
        account.credit(50000)       # $500.00  -> balance: 150000
        account.apply_interest()    # 150000 * 1.05 = 157500
        account.debit(57500)        # -> balance: 100000

        # Then
        self.assertEqual(100000, account.get_balance())  # $1,000.00


if __name__ == "__main__":
    unittest.main()
