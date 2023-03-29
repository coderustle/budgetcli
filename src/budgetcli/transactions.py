"""
This module contains the classes and functions to implement transactions
"""

from enum import Enum
from dataclasses import dataclass
from datetime import date


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
    def __init__(self, entry: Record):
        self.entry = entry
