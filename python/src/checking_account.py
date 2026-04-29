from src.account import Account


class CheckingAccount(Account):
    def __init__(self, account_holder, balance, account_number, overdraft_protection):
        super().__init__(account_holder, balance, account_number)
        # TODO: Implement constructor
        self._account_holder = account_holder
        self._balance = self._to_cents(balance)
        self._account_number = account_number
        self._overdraft_protection = overdraft_protection
            # Initialize a list to track transactions
        self._transactions = []

    def get_overdraft_protection(self):
        # TODO: Implement getter
        return self._overdraft_protection

    def set_overdraft_protection(self, overdraft_protection):
        # TODO: Implement setter
        self._overdraft_protection = overdraft_protection
        
        

    def debit(self, amount):
        # If overdraft_protection is True, don't allow balance to go negative.
        # If overdraft_protection is False, allow balance to go negative.
        amount = self._to_cents(amount)

        if self._overdraft_protection and amount > self._balance:
            print("Insufficient funds. Debit operation not allowed")
            self._transactions.append(
                f"Debit denied: {amount / 100:.2f}, Balance: {self._balance / 100:.2f}"
            )
            return

        self._balance -= amount
        self._transactions.append(
            f"Debited: {amount / 100:.2f}, New Balance: {self._balance / 100:.2f}"
        )