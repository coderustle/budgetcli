"""
This module contains the classes and functions to implement transactions
"""

from enum import Enum
from dataclasses import dataclass
from datetime import date

class TransactionType(Enum):
    INCOME = 1
    OUTCOME = 2

@dataclass
class Transaction:
    """
    This object represents a transaction entry
    """
    tr_type: TransactionType
    tr_date: date
    category: str
    description: str
    amount: float

