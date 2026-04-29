from src.account import Account


class InvestmentAccount(Account):
    def __init__(self, account_holder, balance, account_number, interest_rate):
        super().__init__(account_holder, balance, account_number)
        self.balance = int(balance)  # stored as integer cents
        self.interest_rate = interest_rate

    def get_interest_rate(self):
        return self.interest_rate

    def set_interest_rate(self, interest_rate):
        self.interest_rate = interest_rate

    def apply_interest(self):
        self.balance = round(self.balance * (1 + self.interest_rate))

    def debit(self, amount):
        self.balance -= int(amount)
