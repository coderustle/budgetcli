"""
This module contains the classes and functions to implement transactions
"""

from dataclasses import dataclass
from datetime import date
from enum import Enum

from .data_manager import GoogleSheetManager


class RecordType(Enum):
    INCOME = 1
    OUTCOME = 2


@dataclass
class Record:
    entry_type: RecordType
    entry_date: date
    category: str
    description: str
    amount: float


class Transaction:
    def __init__(self, entry: Record, manager: GoogleSheetManager):
        self.entry = entry

    def __str__(self):
        entry_type = (
            "INCOME"
            if self.entry.entry_type == RecordType.INCOME
            else "OUTCOME"
        )
        return f"{entry_type} - {self.entry.description} - {self.entry.amount}"
