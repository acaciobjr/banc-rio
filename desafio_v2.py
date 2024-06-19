import textwrap
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
    MAX_BALANCE = 2500

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
        elif amount > 500:
            print("\nOperation failed! Withdrawal amount exceeds the limit of 500.")
            return False

        self._balance -= amount
        print("\nWithdrawal successful!")
        return True

    def deposit(self, amount):
        if amount <= 0:
            print("\nOperation failed! Invalid amount.")
            return False
        elif self.balance + amount > self.MAX_BALANCE:
            print("\nOperation failed! Deposit would exceed maximum account balance of 2500.")
            return False

        self._balance += amount
        print("\nDeposit successful!")
        return True

class CheckingAccount(Account):
    def __init__(self, number, customer, limit=500, withdrawal_limit=3):
        super().__init__(number, customer)
        self._limit = limit
        self._withdrawal_limit = withdrawal_limit

    def withdraw(self, amount):
        withdrawals = len([transaction for transaction in self.history.transactions if transaction["type"] == Withdrawal.__name__])

        if amount > self._limit:
            print("\nOperation failed! Withdrawal amount exceeds the limit.")
            return False
        elif withdrawals >= self._withdrawal_limit:
            print("\nOperation failed! Maximum number of withdrawals exceeded.")
            return False
        else:
            return super().withdraw(amount)

    def __str__(self):
        return f"""\
Agency: {self.agency}
Account Number: {self.number}
Account Holder: {self.customer.name}
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

def menu():
    menu = """\n
    ================ MENU ================
    [d] Deposit
    [w] Withdraw
    [s] Statement
    [na] New Account
    [la] List Accounts
    [nc] New Customer
    [q] Quit
    => """
    return input(textwrap.dedent(menu))

def filter_customer(ssn, customers):
    filtered_customers = [customer for customer in customers if customer.ssn == ssn]
    return filtered_customers[0] if filtered_customers else None

def get_customer_account(customer):
    if not customer.accounts:
        print("\nCustomer has no account!")
        return None

    # FIXME: does not allow customer to choose the account
    return customer.accounts[0]

def deposit(customers):
    ssn = input("Enter customer's SSN: ")
    customer = filter_customer(ssn, customers)

    if not customer:
        print("\nCustomer not found!")
        return

    amount = float(input("Enter deposit amount: "))
    transaction = Deposit(amount)

    account = get_customer_account(customer)
    if not account:
        return

    customer.execute_transaction(account, transaction)

def withdraw(customers):
    ssn = input("Enter customer's SSN: ")
    customer = filter_customer(ssn, customers)

    if not customer:
        print("\nCustomer not found!")
        return

    amount = float(input("Enter withdrawal amount: "))
    transaction = Withdrawal(amount)

    account = get_customer_account(customer)
    if not account:
        return

    customer.execute_transaction(account, transaction)

def display_statement(customers):
    ssn = input("Enter customer's SSN: ")
    customer = filter_customer(ssn, customers)

    if not customer:
        print("\nCustomer not found!")
        return

    account = get_customer_account(customer)
    if not account:
        return

    print("\n================ STATEMENT ================")
    transactions = account.history.transactions

    statement = ""
    if not transactions:
        statement = "No transactions found."
    else:
        for transaction in transactions:
            statement += f"\n{transaction['type']}:\n\t$ {transaction['amount']:.2f}"

    print(statement)
    print(f"\nBalance:\n\t$ {account.balance:.2f}")
    print("===========================================")

def create_customer(customers):
    ssn = input("Enter SSN (numbers only): ")
    customer = filter_customer(ssn, customers)

    if customer:
        print("\nCustomer with this SSN already exists!")
        return

    name = input("Enter full name: ")
    birth_date = input("Enter birth date (dd-mm-yyyy): ")
    address = input("Enter address (street, number - neighborhood - city/state): ")

    customer = IndividualCustomer(name=name, birth_date=birth_date, ssn=ssn, address=address)

    customers.append(customer)
    print("\nCustomer successfully created!")

def create_account(account_number, customers, accounts):
    ssn = input("Enter customer's SSN: ")
    customer = filter_customer(ssn, customers)

    if not customer:
        print("\nCustomer not found, account creation process terminated!")
        return

    account = CheckingAccount.new_account(customer=customer, number=account_number)
    accounts.append(account)
    customer.add_account(account)
    print("\nAccount successfully created!")

def list_accounts(accounts):
    for account in accounts:
        print("=" * 50)
        print(textwrap.dedent(str(account)))

def main():
    customers = []
    accounts = []

    while True:
        option = menu()

        if option == "d":
            deposit(customers)

        elif option == "w":
            withdraw(customers)

        elif option == "s":
            display_statement(customers)

        elif option == "nc":
            create_customer(customers)

        elif option == "na":
            account_number = len(accounts) + 1
            create_account(account_number, customers, accounts)

        elif option == "la":
            list_accounts(accounts)

        elif option == "q":
            break

        else:
            print("\nInvalid operation, please select the desired operation again.")

main()
