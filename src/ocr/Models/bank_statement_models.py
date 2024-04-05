
from dataclasses import dataclass


@dataclass
class Transaction:
    """
    Transaction class model
    """
    transaction_date: str
    transaction_details: str
    reference_number: str | None
    debit_amount: float
    credit_amount: float
    balance: float | None

    def __repr__(self):
        return f"{self.transaction_date}, {self.transaction_details}, {self.reference_number}, {self.debit_amount}, {self.credit_amount}, {self.balance}"
    

@dataclass
class AccountStatement:
    """
    Account statement class model
    """
    account_number: str
    account_balance: float
    bank_name: str
    account_statement_period: str
    credit_balance: str | None
    debit_balance: str | None
    transactions: list[Transaction]


    def __repr__(self):
        return f"{self.account_number}, {self.account_statement_period}, {self.account_balance}, {self.transactions}"
    

