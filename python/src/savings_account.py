from src.account import Account


class SavingsAccount(Account):
    def __init__(self, account_holder, balance, account_number, interest_rate):
        super().__init__(account_holder, balance, account_number)
        self.interest_rate = interest_rate

    def get_interest_rate(self):
        return self.interest_rate

    def set_interest_rate(self, interest_rate):
        self.interest_rate = interest_rate

    def apply_interest(self):
        interest_amount = self._to_cents(self.get_balance() * self.interest_rate)
        self._balance += interest_amount
        self._transactions.append(
            f"Interest applied: {self._format_cents(interest_amount)}, New Balance: {self._format_cents(self._balance)}"
        )

    def debit(self, amount):
        amount_in_cents = self._to_cents(amount)
        if self._balance - amount_in_cents < 0:
            self._transactions.append(
                f"Debit denied: {self._format_cents(amount_in_cents)}, Balance: {self._format_cents(self._balance)}"
            )
            return True
        self._balance -= amount_in_cents
        self._transactions.append(
            f"Debited: {self._format_cents(amount_in_cents)}, New Balance: {self._format_cents(self._balance)}"
        )
        return False
