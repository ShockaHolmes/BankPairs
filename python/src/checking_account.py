from src.account import Account


class CheckingAccount(Account):
    def __init__(self, account_holder, balance, account_number, overdraft_protection):
        super().__init__(account_holder, balance, account_number)
        self.balance = int(balance)  # stored as integer cents
        self.overdraft_protection = overdraft_protection

    def get_overdraft_protection(self):
        return self.overdraft_protection

    def set_overdraft_protection(self, overdraft_protection):
        self.overdraft_protection = overdraft_protection

    def debit(self, amount):
        amount_cents = int(amount)
        if self.overdraft_protection:
            if self.balance - amount_cents >= 0:
                self.balance -= amount_cents
        else:
            self.balance -= amount_cents
