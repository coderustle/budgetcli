from decimal import Decimal
from datetime import datetime

from budgetcli.transactions import Transaction


def test_transaction_instance():
    """Test that a transaction instance is created"""
    transaction = Transaction(
        datetime.now(),
        "Salary",
        "Salary for January",
        Decimal(0.0),
        Decimal(0.0),
    )
    assert isinstance(transaction, Transaction)


def test_transaction_from_sheet_row():
    """Test that a transaction instance is created from a sheet row"""
    transaction = Transaction.from_sheet_row(
        [
            "01/01/2021",
            "category",
            "Salary for January",
            "0.0",
            "1000.0",
        ]
    )
    assert isinstance(transaction, Transaction)
