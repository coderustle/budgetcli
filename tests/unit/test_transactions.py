from decimal import Decimal

from budgetcli.transactions import Transaction


def test_transaction_instance():
    """Test that a transaction instance is created"""
    transaction = Transaction(
        "01/01/2021",
        "Salary",
        "Salary for January",
        Decimal(0.0),
        Decimal(1000.0),
    )
    assert isinstance(transaction, Transaction)


def test_transaction_from_sheet_row():
    """Test that a transaction instance is created from a sheet row"""
    transaction = Transaction.from_sheet_row(
        [
            "01/01/2021",
            "Salary",
            "Salary for January",
            "0.0",
            "1000.0",
        ]
    )
    assert isinstance(transaction, Transaction)
