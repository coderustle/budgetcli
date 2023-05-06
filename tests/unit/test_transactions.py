from unittest.mock import patch, MagicMock, AsyncMock

import pytest

from budgetcli.data_manager import ManagerFactory, AbstractDataManager


@pytest.fixture
def manager():
    return ManagerFactory.create_manager_for("transactions")


@pytest.fixture
def return_json_list(transactions_list_response):
    def result():
        return transactions_list_response

    return result


@pytest.fixture
def fake_coro():
    async def coro():
        return None

    return coro


@pytest.fixture
def fake_sheet_coro():
    async def mock_coro():
        return {
            "sheetId": 345247012,
            "title": "TRANSACTIONS",
            "index": 1,
            "sheetType": "GRID",
            "gridProperties": {"rowCount": 1000, "columnCount": 26},
        }

    return mock_coro


@pytest.fixture
def transactions():
    return [
        ["05-05-2023", "salary", "", "200", "0"],
        ["06-05-2023", "rent", "", "0", "100"],
    ]


@pytest.mark.asyncio
async def test_init_sheet_exists(manager, fake_sheet_coro, fake_coro):
    """Test init sheet get sheet"""
    manager._update = MagicMock()
    manager._update.return_value = fake_coro()

    manager._get_sheet = MagicMock()
    manager._get_sheet.return_value = fake_sheet_coro()

    with patch("budgetcli.data_manager.update_config") as mock_config:
        await manager.init()
        manager._get_sheet.assert_called_once()
        mock_config.assert_called_once()
        manager._update.assert_called_once()


@pytest.mark.asyncio
async def test_init_sheet_create(manager, fake_sheet_coro, fake_coro):
    """Test init sheet create"""

    manager._update = MagicMock()
    manager._update.return_value = fake_coro()

    manager._get_sheet = MagicMock()
    manager._get_sheet.return_value = fake_coro()

    manager._create_sheet = MagicMock()
    manager._create_sheet.return_value = fake_sheet_coro()

    with patch("budgetcli.data_manager.update_config") as mock_config:
        await manager.init()
        manager._get_sheet.assert_called_once()
        manager._create_sheet.assert_called_once()
        mock_config.assert_called_once()
        manager._update.assert_called_once()


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


@pytest.mark.asyncio
async def test_get_records(manager, return_json_list):
    """Test get transactions method"""

    # build url
    params = "majorDimension=ROWS"
    url = f"{manager.base_url}/values/TRANSACTIONS!A2:E101?{params}"

    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json = return_json_list

    session_mock = AsyncMock()
    session_mock.get.return_value = mock_response

    manager.session = session_mock

    result = await manager.get_records()
    
    session_mock.get.assert_called_once_with(url)
    mock_response.raise_for_status.assert_called_once()
    assert result


@pytest.mark.asyncio
async def test_get_records_rows_option(manager, transactions):
    """Test get transactions with rows option"""
    expected = [["2023-04-05", "category", " ", "20", "0"]]
    with patch.object(AbstractDataManager, "_list") as mock_list:
        mock_list.return_value = expected
        result = await manager.get_records(rows=1)
        assert len(result) == 1


# @pytest.mark.skip
@pytest.mark.asyncio
async def test_get_records_for_month(manager, transactions_month_response):
    """Test get transactions for month"""

    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.text = transactions_month_response

    session_mock = AsyncMock()
    session_mock.get.return_value = mock_response

    manager.session = session_mock

    result = await manager.get_records_for_month(month=5)

    session_mock.get.assert_called_once()
    mock_response.raise_for_status.assert_called_once()
    assert result
