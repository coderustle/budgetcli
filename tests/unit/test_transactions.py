from unittest.mock import MagicMock, AsyncMock

import pytest

from budgetcli.data_manager import TransactionDataManager


@pytest.mark.asyncio
async def test_init_sheet_exists(init_get_sheet, transactions_update_response):
    """Test init sheet get sheet"""

    session_mock = AsyncMock()

    get_response_mock = MagicMock()
    get_response_mock.raise_for_status.return_value = None
    get_response_mock.json = init_get_sheet

    session_mock.get.return_value = get_response_mock

    put_response_mock = MagicMock()
    put_response_mock.raise_for_status.return_value = None
    put_response_mock.json = transactions_update_response

    session_mock.put.return_value = put_response_mock

    manager = TransactionDataManager(session=session_mock)

    await manager.init()

    session_mock.get.assert_called_once()
    session_mock.put.assert_called_once()
    get_response_mock.raise_for_status.assert_called_once()


@pytest.mark.asyncio
async def test_init_sheet_create(
    transactions_init_create_sheet, transactions_update_response
):
    """Test init sheet create"""

    session_mock = AsyncMock()

    get_response_mock = MagicMock()
    get_response_mock.raise_for_status.return_value = None
    get_response_mock.json = lambda: {}

    session_mock.get.return_value = get_response_mock

    post_response_mock = MagicMock()
    post_response_mock.raise_for_status.return_value = None
    post_response_mock.json = transactions_init_create_sheet

    session_mock.post.return_value = post_response_mock

    put_response_mock = MagicMock()
    put_response_mock.raise_for_status.return_value = None
    put_response_mock.json = transactions_update_response

    session_mock.put.return_value = put_response_mock

    manager = TransactionDataManager(session=session_mock)

    await manager.init()

    url = f"{manager.base_url}/:batchUpdate"
    data = {
        "requests": [{"addSheet": {"properties": {"title": "TRANSACTIONS"}}}]
    }
    session_mock.post.assert_called_once_with(url, json=data)
    session_mock.put.assert_called_once()


@pytest.mark.asyncio
async def test_update_method(transactions_update_response):
    """Test transactions update method"""
    headers = "DATE CATEGORY DESCRIPTION INCOME OUTCOME"

    response_mock = MagicMock()
    response_mock.raise_for_status.return_value = None
    response_mock.json = transactions_update_response

    session_mock = AsyncMock()
    session_mock.put.return_value = response_mock

    manager = TransactionDataManager(session=session_mock)

    result = await manager.update(values=headers.split(), a1="A1")
    params = "valueInputOption=USER_ENTERED"
    url = f"{manager.base_url}/values/TRANSACTIONS!A1?{params}"
    data = {
        "range": "TRANSACTIONS!A1",
        "majorDimension": "ROWS",
        "values": [["DATE", "CATEGORY", "DESCRIPTION", "INCOME", "OUTCOME"]],
    }
    session_mock.put.assert_called_once_with(url, json=data)
    response_mock.raise_for_status.assert_called_once()
    assert result


@pytest.mark.asyncio
async def test_append_method(transactions_append_response):
    """Test transactions append method with values"""
    values = "20-04-2023 category description 0 200"

    response_mock = MagicMock()
    response_mock.raise_for_status.return_value = None
    response_mock.json = transactions_append_response

    session_mock = AsyncMock()
    session_mock.post.return_value = response_mock

    manager = TransactionDataManager(session=session_mock)

    result = await manager.append(values=values.split())
    params = "valueInputOption=USER_ENTERED"
    notation = "TRANSACTIONS!A2:E"
    url = f"{manager.base_url}/values/{notation}:append?{params}"
    data = {
        "majorDimension": "ROWS",
        "values": [["20-04-2023", "category", "description", "0", "200"]],
    }
    session_mock.post.assert_called_once_with(url, json=data)
    response_mock.raise_for_status.assert_called_once()
    assert result


@pytest.mark.asyncio
async def test_get_records(transactions_list_response):
    """Test get transactions method"""

    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json = transactions_list_response

    session_mock = AsyncMock()
    session_mock.get.return_value = mock_response

    manager = TransactionDataManager(session=session_mock)

    # build url
    params = "majorDimension=ROWS"
    url = f"{manager.base_url}/values/TRANSACTIONS!A2:E101?{params}"

    result = await manager.get_records()

    session_mock.get.assert_called_once_with(url)
    mock_response.raise_for_status.assert_called_once()
    assert result
    assert len(result) == 100


@pytest.mark.asyncio
async def test_get_records_rows_option(transactions_rows_response):
    """Test get transactions with rows option"""

    response_mock = MagicMock()
    response_mock.raise_for_status.return_value = None
    response_mock.json = transactions_rows_response

    session_mock = AsyncMock()
    session_mock.get.return_value = response_mock

    manager = TransactionDataManager(session=session_mock)

    # build url
    params = "majorDimension=ROWS"
    url = f"{manager.base_url}/values/TRANSACTIONS!A2:E2?{params}"

    result = await manager.get_records(rows=1)
    session_mock.get.assert_called_once_with(url)
    response_mock.raise_for_status.assert_called_once()
    assert len(result) == 1


@pytest.mark.asyncio
async def test_get_records_for_month(transactions_month_response):
    """Test get transactions for month"""

    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.text = transactions_month_response

    session_mock = AsyncMock()
    session_mock.get.return_value = mock_response

    manager = TransactionDataManager(session=session_mock)

    result = await manager.get_records_for_month(month=5)

    session_mock.get.assert_called_once()
    mock_response.raise_for_status.assert_called_once()
    assert result
