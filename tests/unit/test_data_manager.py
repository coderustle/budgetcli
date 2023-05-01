import pytest
import unittest

from rich.pretty import pprint

from budgetcli.data_manager import ManagerFactory


class TestTransactionDataManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manager = ManagerFactory.create_manager_for("transactions")

    @pytest.mark.asyncio
    async def test_create_sheet(self):
        """Test if sheet with given name exists"""