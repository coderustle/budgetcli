import pytest

from budgetcli.data_manager import ManagerFactory


@pytest.fixture()
def manager():
    return ManagerFactory.create_manager_for("budgets")


@pytest.mark.asyncio
def test_init_sheet_exists(manager):
    """Test init sheet get sheet"""
    print(manager)
