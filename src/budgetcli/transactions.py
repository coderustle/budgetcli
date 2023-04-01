"""
This module contains the classes and functions to implement transactions
"""

from dataclasses import dataclass
from enum import Enum

from .abstract import Command
from .data_manager import GoogleSheetManager


class TransactionType(Enum):
    INCOME = "income"
    OUTCOME = "outcome"


@dataclass
class Transaction:
    date: str
    category: str
    description: str
    amount: float

    def __post_init__(self):
        pass

    def to_list(self):
        return [
            self.date,
            self.category,
            self.description,
            self.amount,
        ]


class AddTransactionCommand(Command):
    def __init__(self, transaction: Transaction, manager: GoogleSheetManager):
        self.transaction = transaction
        self.manager = manager

    def execute(self):
        self.manager.add_transaction(self.transaction.to_list())

    def __str__(self):
        return f"Add transaction: {self.entry.description}"
