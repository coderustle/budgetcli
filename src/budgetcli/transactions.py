"""
This module contains the classes and functions to implement transactions
"""

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum


class TransactionType(Enum):
    INCOME = "income"
    OUTCOME = "outcome"


@dataclass
class Transaction:
    date: str
    category: str
    description: str
    outcome: Decimal
    income: Decimal

    @classmethod
    def from_sheet_row(cls, row: list):
        return cls(
            row[0],
            row[1],
            row[2],
            Decimal(row[3]),
            Decimal(row[4]),
        )

    def to_sheet_row(self):
        return [
            self.date,
            self.category,
            self.description,
            self.amount,
        ]
