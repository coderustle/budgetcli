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


@pytest.mark.asyncio
async def test_append_method_with_values(manager):
    """Test transactions append method with values"""
    values = "20-04-2023 category description 0 200"
    return_values = {
        "spreadsheetId": "Ckwbcjyo0WjEgmF8kFsWl7etoc",
        "tableRange": "TRANSACTIONS!A2:E4",
        "updates": {
            "spreadsheetId": "Ckwbcjyo0WjEgmF8kFsWl7etoc",
            "updatedRange": "TRANSACTIONS!A5:E5",
            "updatedRows": 1,
            "updatedColumns": 5,
            "updatedCells": 5,
        },
    }
    with patch.object(AbstractDataManager, "_append") as append_mock:
        append_mock.return_value = return_values
        result = await manager.append(values=values.split())
        append_mock.assert_called_once()
        assert result


@pytest.mark.asyncio
async def test_append_method_with_no_values(manager):
    """Test transactions append method with no values"""
    values = "20-04-2023 category description 0 200"
    with patch.object(AbstractDataManager, "_append") as append_mock:
        append_mock.return_value = {}
        result = await manager.append(values=values.split())
        append_mock.assert_called_once()
        assert not result
