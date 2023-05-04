from unittest.mock import patch

import pytest
from budgetcli.data_manager import ManagerFactory, AbstractDataManager


@pytest.fixture
def manager():
    return ManagerFactory.create_manager_for("transactions")


@pytest.mark.slow
@pytest.mark.asyncio
async def test_init_sheet(manager, capsys):
    """Test init sheet method"""
    await manager.init()
    output = capsys.readouterr()
    text = "✔ transactions_sheet_index was updated"
    assert text in output.out


@pytest.mark.asyncio
async def test_update_method_with_values(manager):
    """Test transactions update method"""
    headers = "DATE CATEGORY DESCRIPTION INCOME OUTCOME"
    return_values = {
        "spreadsheetId": "0",
        "updatedRange": "0",
        "updatedRows": "0",
        "updatedColumns": "0",
        "updatedCells": "0",
    }
    with patch.object(AbstractDataManager, "_update") as update_mock:
        update_mock.return_values = return_values
        result = await manager.update(values=headers.split(), a1="A1")
        update_mock.assert_called_once()
        assert result


@pytest.mark.asyncio
async def test_update_method_no_values(manager):
    """Test transactions update method no values"""
    with patch.object(AbstractDataManager, "_update") as update_mock:
        update_mock.return_value = {}
        result = await manager.update(values=["data"], a1="A1")
        update_mock.assert_called_once()
        assert not result
