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
    income: Decimal
    outcome: Decimal

    @classmethod
    def from_sheet_row(cls, row: list):
        return cls(
            row[0],             # date
            row[1],             # category
            row[2],             # description
            Decimal(row[3]),    # income
            Decimal(row[3]),    # outcome
        )

    def to_sheet_row(self):
        return [
            self.date,
            self.category,
            self.description,
            self.income,
            self.outcome,
        ]
