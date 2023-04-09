from typing import List
from unittest.mock import patch

import pytest

from budgetcli.data_manager import TransactionDataManager, ManagerFactory


@pytest.fixture
def transaction_manager():
    """A pytest fixture to return transaction manager"""
    return ManagerFactory.create_manager_for("transactions")


def test_transaction__manager_instance(transaction_manager):
    """Test instance of the GoogleSheetManager"""
    assert transaction_manager is not None
    assert isinstance(transaction_manager, TransactionDataManager)


def test_list_transactions_operation(transaction_manager):
    """Test list transactions"""
    to_patch = "budgetcli.data_manager.TransactionDataManager._list"
    return_value = {"values": [["row1"], ["row2"]]}

    with patch(to_patch, return_value=return_value, autospec=True):
        result = transaction_manager.list_transactions()
        assert isinstance(result, List)


def test_list_transactions_operation_count(transaction_manager):
    """Test return only 3 transactions"""

    to_patch = "budgetcli.data_manager.TransactionDataManager._list"
    return_value = {"values": [["row1"], ["row2"], ["row3"], ["row4"]]}

    with patch(to_patch, return_value=return_value, autospec=True):
        values = transaction_manager.list_transactions(rows=3)
        if isinstance(values, List):
            assert len(values[1:]) == 3
