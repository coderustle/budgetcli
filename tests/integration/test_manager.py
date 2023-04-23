import pytest
from rich.pretty import pprint

from budgetcli.data_manager import ManagerFactory


class TestTransactionDataManager:
    @pytest.mark.asyncio
    async def test_sheet_exists(self):
        """Test if sheet with given name exists"""
        manager = ManagerFactory.create_manager_for("transactions")
        if manager:
            result = await manager.sheet_exists("TRANSACTIONS")
            assert result

    @pytest.mark.asyncio
    async def test_create_sheet(self):
        """Test create sheet with given name"""
        manager = ManagerFactory.create_manager_for("transactions")
        if manager:
            result = await manager.create_sheet("TRANSACTIONS")
            assert not result

    @pytest.mark.asyncio
    async def test_get_transactions(self):
        """Test query transactions"""
        manager = ManagerFactory.create_manager_for("transactions")
        if manager:
            result = await manager.get_transactions_for_month(4)
            pprint(result, expand_all=True)
            assert isinstance(result, list)
            assert len(result) == 3
