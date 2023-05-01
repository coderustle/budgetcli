"""
This module contains the classes and functions to implement transactions
"""

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from enum import Enum

from rich import print


def validate_amount(amount: str) -> Decimal | None:
    """A utility function to validate the transaction amount"""
    try:
        return Decimal(amount)
    except InvalidOperation:
        print(":x: Invalid amount provided")
    return None


def validate_date(date_str: str) -> date | None:
    """A utility function to validate the transaction dates"""
    date_formats = ["%Y-%m-%d", "%Y/%m/%d", "%d/%m/%Y", "%d-%m-%Y"]
    for date_format in date_formats:
        try:
            parsed_date = datetime.strptime(date_str, date_format).date()
            return parsed_date
        except ValueError:
            pass
    print(":x: Invalid date provided")
    print(f"Supported formats are: {'  '.join(date_formats)}")
    return None


class TransactionType(Enum):
    """
    An enum to represent the type of transaction
    """

    INCOME = "income"
    OUTCOME = "outcome"


@dataclass
class Transaction:
    """
    A class to represent a transaction
    """

    date: date
    category: str
    description: str
    income: Decimal = Decimal(0)
    outcome: Decimal = Decimal(0)

    @classmethod
    def from_sheet_row(cls, row: list):
        """
        A method to create a transaction from a list of strings
        """
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
        """
        A method to convert the transaction to a list of strings
        """
        date_format = "%d-%m-%Y"
        return [
            self.date.strftime(date_format),
            self.category,
            self.description,
            str(self.income),
            str(self.outcome),
        ]


@dataclass
class Category:
    """
    Represents a category object
    """

    name: str

    def __post_init__(self):
        self.name = self.name.lower()

    @classmethod
    def from_sheet_row(cls, row: list):
        """
        Create a category object from a list of strings
        """
        return cls(row[0])

    def to_sheet_row(self) -> list[str]:
        """
        Return a list with values
        """
        return [self.name]
