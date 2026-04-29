import unittest
from src.person import Person
from src.business import Business
from src.checking_account import CheckingAccount


# All monetary values are integers representing cents.
# e.g. 100000 cents = $1,000.00


class TestCheckingAccount(unittest.TestCase):

    def test_constructor_with_person(self):
        # Given
        account_holder = Person("John", "Doe", "john@example.com", "555-1234")
        balance = 100000  # $1,000.00 in cents
        account_number = "CHK001"
        overdraft_protection = True

        # When
        account = CheckingAccount(account_holder, balance, account_number, overdraft_protection)

        # Then
        self.assertIsNotNone(account)
        self.assertEqual(account_holder, account.get_account_holder())
        self.assertEqual(balance, account.get_balance())
        self.assertEqual(account_number, account.get_account_number())

    def test_constructor_with_business(self):
        # Given
        account_holder = Business("Acme Corp")
        balance = 500000  # $5,000.00 in cents
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
        account = CheckingAccount(account_holder, 100000, "CHK003", expected_overdraft_protection)

        # When
        actual_overdraft_protection = account.get_overdraft_protection()

        # Then
        self.assertEqual(expected_overdraft_protection, actual_overdraft_protection)

    def test_set_overdraft_protection(self):
        # Given
        account_holder = Person("Bob", "Jones", "bob@example.com", "555-9999")
        account = CheckingAccount(account_holder, 100000, "CHK004", True)

        # When
        account.set_overdraft_protection(False)

        # Then
        self.assertFalse(account.get_overdraft_protection())

    def test_debit_with_overdraft_protection_enabled(self):
        # Given
        account_holder = Person("Alice", "Brown", "alice@example.com", "555-1111")
        account = CheckingAccount(account_holder, 50000, "CHK005", True)  # $500.00

        # When - Attempting to overdraw
        account.debit(60000)  # $600.00

        # Then - Balance should remain unchanged (overdraft protection enabled)
        self.assertEqual(50000, account.get_balance())

    def test_debit_with_overdraft_protection_disabled(self):
        # Given
        account_holder = Person("Charlie", "Wilson", "charlie@example.com", "555-2222")
        account = CheckingAccount(account_holder, 50000, "CHK006", False)  # $500.00

        # When - Attempting to overdraw
        account.debit(60000)  # $600.00

        # Then - Balance goes negative (overdraft protection disabled)
        self.assertEqual(-10000, account.get_balance())  # -$100.00

    def test_debit_with_sufficient_funds(self):
        # Given
        account_holder = Person("David", "Miller", "david@example.com", "555-3333")
        account = CheckingAccount(account_holder, 100000, "CHK007", True)  # $1,000.00

        # When
        account.debit(30000)  # $300.00

        # Then
        self.assertEqual(70000, account.get_balance())  # $700.00

    def test_credit_in_checking_account(self):
        # Given
        account_holder = Person("Eve", "Davis", "eve@example.com", "555-4444")
        account = CheckingAccount(account_holder, 100000, "CHK008", True)  # $1,000.00

        # When
        account.credit(50000)  # $500.00

        # Then
        self.assertEqual(150000, account.get_balance())  # $1,500.00

    def test_multiple_transactions(self):
        # Given
        account_holder = Person("Frank", "Garcia", "frank@example.com", "555-5555")
        account = CheckingAccount(account_holder, 100000, "CHK009", False)  # $1,000.00

        # When
        account.credit(20000)   # +$200.00 -> 120000
        account.debit(30000)    # -$300.00 -> 90000
        account.credit(10000)   # +$100.00 -> 100000

        # Then
        self.assertEqual(100000, account.get_balance())  # $1,000.00


if __name__ == "__main__":
    unittest.main()
