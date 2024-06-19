from abc import ABC, abstractmethod
from datetime import datetime


class Customer:
    def __init__(self, address):
        self.address = address
        self.accounts = []

    def execute_transaction(self, account, transaction):
        transaction.register(account)

    def add_account(self, account):
        self.accounts.append(account)


class IndividualCustomer(Customer):
    def __init__(self, name, birth_date, ssn, address):
        super().__init__(address)
        self.name = name
        self.birth_date = birth_date
        self.ssn = ssn


class Account:
    def __init__(self, number, customer):
        self._balance = 0
        self._number = number
        self._agency = "0001"
        self._customer = customer
        self._history = TransactionHistory()

    @classmethod
    def new_account(cls, customer, number):
        return cls(number, customer)

    @property
    def balance(self):
        return self._balance

    @property
    def number(self):
        return self._number

    @property
    def agency(self):
        return self._agency

    @property
    def customer(self):
        return self._customer

    @property
    def history(self):
        return self._history

    def withdraw(self, amount):
        if amount > self.balance:
            print("\nOperation failed! Insufficient balance.")
            return False
        elif amount <= 0:
            print("\nOperation failed! Invalid amount.")
            return False

        self._balance -= amount
        print("\nWithdrawal successful!")
        return True

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print("\nDeposit successful!")
            return True
        else:
            print("\nOperation failed! Invalid amount.")
            return False


class CheckingAccount(Account):
    def __init__(self, number, customer, limit=500, withdrawal_limit=3):
        super().__init__(number, customer)
        self.limit = limit
        self.withdrawal_limit = withdrawal_limit

    def withdraw(self, amount):
        withdrawals = len([transaction for transaction in self.history.transactions if transaction["type"] == Withdrawal.__name__])

        if amount > self.limit:
            print("\nOperation failed! Withdrawal amount exceeds limit.")
            return False
        elif withdrawals >= self.withdrawal_limit:
            print("\nOperation failed! Maximum number of withdrawals exceeded.")
            return False
        else:
            return super().withdraw(amount)

    def __str__(self):
        return f"""\
Agency:\t{self.agency}
Account Number:\t{self.number}
Account Holder:\t{self.customer.name}
"""


class TransactionHistory:
    def __init__(self):
        self._transactions = []

    @property
    def transactions(self):
        return self._transactions

    def add_transaction(self, transaction):
        self._transactions.append({
            "type": transaction.__class__.__name__,
            "amount": transaction.amount,
            "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        })


class Transaction(ABC):
    @property
    @abstractmethod
    def amount(self):
        pass

    @abstractmethod
    def register(self, account):
        pass


class Withdrawal(Transaction):
    def __init__(self, amount):
        self._amount = amount

    @property
    def amount(self):
        return self._amount

    def register(self, account):
        if account.withdraw(self.amount):
            account.history.add_transaction(self)


class Deposit(Transaction):
    def __init__(self, amount):
        self._amount = amount

    @property
    def amount(self):
        return self._amount

    def register(self, account):
        if account.deposit(self.amount):
            account.history.add_transaction(self)
