from abc import ABC, abstractmethod


class Account(ABC):
    def __init__(self, account_holder, balance, account_number):
        # TODO: Implement constructor
        self._account_holder = account_holder
        self._balance = self._to_cents(balance)
        self._account_number = account_number
        # Initialize a list to track transactions
        self._transactions = []

    def _to_cents(self, value):
        # Store all money as integer cents.
        value_str = str(value).strip()
        is_negative = value_str.startswith("-")
        if is_negative:
            value_str = value_str[1:]

        if "." in value_str:
            dollars_part, fractional_part = value_str.split(".", 1)
        else:
            dollars_part, fractional_part = value_str, ""

        if dollars_part == "":
            dollars_part = "0"

        two_digits = (fractional_part + "00")[:2]
        third_digit = (fractional_part + "000")[2]

        cents = int(dollars_part) * 100 + int(two_digits)
        if third_digit >= "5":
            cents += 1

        return -cents if is_negative else cents

    def _format_cents(self, cents):
        return f"{cents / 100:.2f}"

    def get_account_holder(self):
        # TODO: Implement getter
        return self._account_holder

    def get_balance(self):
        # TODO: Implement getter
        return float(f"{self._balance / 100:.2f}")

    def set_balance(self, balance):
        # TODO: Implement setter
        self._balance = self._to_cents(balance)

    def get_account_number(self):
        # TODO: Implement getter
        return self._account_number

    def get_account_type(self):
        return self.__class__.__name__

    def get_holder_name(self):
        holder = self.get_account_holder()

        if hasattr(holder, "get_first_name") and hasattr(holder, "get_last_name"):
            return f"{holder.get_first_name()} {holder.get_last_name()}"

        if hasattr(holder, "get_business_name"):
            return holder.get_business_name()

        return str(holder)

    def get_holder_email(self):
        holder = self.get_account_holder()
        if hasattr(holder, "get_email"):
            return holder.get_email()
        return ""

    def get_holder_phone_number(self):
        holder = self.get_account_holder()
        if hasattr(holder, "get_phone_number"):
            return holder.get_phone_number()
        return ""

    def deposit(self, amount):
        self.credit(amount)
        return self.get_balance()

    def withdraw(self, amount):
        return self.debit(amount)

    def credit(self, amount):
        # TODO: Implement credit method (add money to account)
        amount = self._to_cents(amount)
        self._balance += amount
        # TODO: Record this transaction
        self._transactions.append(
            f"Credited: {self._format_cents(amount)}, New Balance: {self._format_cents(self._balance)}"
        )

    def debit(self, amount):
        # TODO: Implement debit method (remove money from account)
        amount = self._to_cents(amount)
        self._balance -= amount
        # TODO: Record this transaction
        self._transactions.append(
            f"Debited: {self._format_cents(amount)}, New Balance: {self._format_cents(self._balance)}"
        )

    def get_transactions(self):
        # TODO: Implement method to return transaction history
        return self._transactions

    def get_account_summary(self):
        return {
            "customer_name": self.get_holder_name(),
            "account_type": self.get_account_type(),
            "account_number": self.get_account_number(),
            "balance": f"{self.get_balance():.2f}",
            "email": self.get_holder_email(),
            "phone_number": self.get_holder_phone_number(),
            "transactions": list(self.get_transactions()),
        }
