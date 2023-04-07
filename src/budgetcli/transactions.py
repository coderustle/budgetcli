"""
This module contains the classes and functions to implement transactions
"""

from dataclasses import dataclass
from datetime import datetime, date
from decimal import Decimal, InvalidOperation
from enum import Enum

from rich import print


def validate_amount(amount: str) -> Decimal | None:
    """An utility function to validate the transaction amount"""
    try:
        return Decimal(amount)
    except InvalidOperation:
        print(":x: Invalid amount provided")


def validate_date(date_str: str) -> date | None:
    """An utility function to validate the transaction dates"""
    date_formats = ["%Y-%m-%d", "%Y/%m/%d", "%d/%m/%Y", "%d-%m-%Y"]
    for format in date_formats:
        try:
            parsed_date = datetime.strptime(date_str, format).date()
            return parsed_date
        except ValueError:
            pass
    print(":x: Invalid date provided")
    print(f"Supported formats are: {'  '.join(date_formats)}")


class TransactionType(Enum):
    INCOME = "income"
    OUTCOME = "outcome"


@dataclass
class Transaction:
    date: date
    category: str
    description: str
    income: Decimal = Decimal(0)
    outcome: Decimal = Decimal(0)

    @classmethod
    def from_sheet_row(cls, row: list):
        parsed_date = validate_date(row[0])
        if parsed_date:
            return cls(
                parsed_date,  # date
                row[1],  # category
                row[2],  # description
                Decimal(row[3]),  # income
                Decimal(row[4]),  # outcome
            )

    def to_sheet_row(self):
        date_format = "%d-%m-%Y"
        return [
            self.date.strftime(date_format),
            self.category,
            self.description,
            str(self.income),
            str(self.outcome),
        ]
