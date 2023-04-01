from datetime import date

import pytest
from budgetcli.data_manager import GoogleSheetManager
from budgetcli.transactions import Record, RecordType, Transaction


@pytest.fixture
def record_fixture():
    """Fixture for a record instance"""
    return Record(
        RecordType.INCOME,
        date(2021, 1, 1),
        "Salary",
        "Salary for January",
        1000.0,
    )


def test_transaction_instance(record_fixture):
    """Test that a transaction instance is created"""
    entry = record_fixture
    transaction = Transaction(entry, GoogleSheetManager())
    assert isinstance(transaction, Transaction)


def test_transaction_str(record_fixture):
    """Test that the transaction string representation is correct"""
    entry = record_fixture
    transaction = Transaction(entry, GoogleSheetManager())
    assert str(transaction) == "INCOME - Salary for January - 1000.0"
