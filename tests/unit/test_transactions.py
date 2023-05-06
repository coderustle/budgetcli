from unittest.mock import patch, MagicMock, AsyncMock

import pytest

from budgetcli.data_manager import ManagerFactory, AbstractDataManager


@pytest.fixture
def manager():
    return ManagerFactory.create_manager_for("transactions")


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


@pytest.mark.asyncio
async def test_init_sheet_exists(
    manager, transactions_init_get_sheet, transactions_update_response
):
    """Test init sheet get sheet"""

    session_mock = AsyncMock()

    get_response_mock = MagicMock()
    get_response_mock.raise_for_status.return_value = None
    get_response_mock.json = transactions_init_get_sheet

    session_mock.get.return_value = get_response_mock

    put_response_mock = MagicMock()
    put_response_mock.raise_for_status.return_value = None
    put_response_mock.json = transactions_update_response

    session_mock.put.return_value = put_response_mock

    manager.session = session_mock

    with patch("budgetcli.data_manager.update_config") as mock_config:
        await manager.init()
        mock_config.assert_called_once()
        session_mock.get.assert_called_once()
        session_mock.put.assert_called_once()
        get_response_mock.raise_for_status.assert_called_once()


@pytest.mark.asyncio
async def test_init_sheet_create(
    manager, transactions_init_get_sheet, transactions_update_response
):
    """Test init sheet create"""

    session_mock = AsyncMock()

    get_response_mock = MagicMock()
    get_response_mock.raise_for_status.return_value = None
    get_response_mock.json = transactions_init_get_sheet

    session_mock.get.return_value = get_response_mock

    put_response_mock = MagicMock()
    put_response_mock.raise_for_status.return_value = None
    put_response_mock.json = transactions_update_response

    session_mock.put.return_value = put_response_mock

    manager.session = session_mock

    with patch("budgetcli.data_manager.update_config") as mock_config:
        await manager.init()
        mock_config.assert_called_once()
        session_mock.get.assert_called_once()
        session_mock.put.assert_called_once()
        get_response_mock.raise_for_status.assert_called_once()


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
async def test_get_records(manager, transactions_list_response):
    """Test get transactions method"""

    # build url
    params = "majorDimension=ROWS"
    url = f"{manager.base_url}/values/TRANSACTIONS!A2:E101?{params}"

    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json = transactions_list_response

    session_mock = AsyncMock()
    session_mock.get.return_value = mock_response

    manager.session = session_mock

    result = await manager.get_records()

    session_mock.get.assert_called_once_with(url)
    mock_response.raise_for_status.assert_called_once()
    assert result
    assert len(result) == 100


@pytest.mark.asyncio
async def test_get_records_rows_option(manager, transactions_rows_response):
    """Test get transactions with rows option"""

    # build url
    params = "majorDimension=ROWS"
    url = f"{manager.base_url}/values/TRANSACTIONS!A2:E2?{params}"

    response_mock = MagicMock()
    response_mock.raise_for_status.return_value = None
    response_mock.json = transactions_rows_response

    session_mock = AsyncMock()
    session_mock.get.return_value = response_mock

    manager.session = session_mock

    result = await manager.get_records(rows=1)
    session_mock.get.assert_called_once_with(url)
    response_mock.raise_for_status.assert_called_once()
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
