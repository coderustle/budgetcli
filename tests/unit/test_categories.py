from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from budgetcli.data_manager import ManagerFactory


@pytest.fixture
def manager():
    return ManagerFactory.create_manager_for("categories")


@pytest.mark.asyncio
async def test_init_sheet_exists(
    manager, categories_init_get_sheet, categories_update_response
):
    """Test get sheet in init"""

    session_mock = AsyncMock()

    get_response_mock = MagicMock()
    get_response_mock.raise_for_status.return_value = None
    get_response_mock.json = categories_init_get_sheet

    session_mock.get.return_value = get_response_mock

    put_response_mock = MagicMock()
    put_response_mock.raise_for_status.return_value = None
    put_response_mock.json = categories_update_response

    session_mock.put.return_value = put_response_mock

    manager.session = session_mock

    with patch("budgetcli.data_manager.update_config") as mock_config:
        await manager.init()
        session_mock.get.assert_called_once()
        session_mock.put.assert_called_once()
        get_response_mock.raise_for_status.assert_called_once()
        put_response_mock.raise_for_status.assert_called_once()
        mock_config.assert_called_once()


@pytest.mark.asyncio
async def test_init_sheet_create(
    manager, categories_update_response, categories_init_create_sheet
):
    """Test init sheet create new sheet"""

    session_mock = AsyncMock()

    get_response_mock = MagicMock()
    get_response_mock.raise_for_status.return_value = None
    get_response_mock.json = lambda: {}

    session_mock.get.return_value = get_response_mock

    post_response_mock = MagicMock()
    post_response_mock.raise_for_status.return_value = None
    post_response_mock.json = categories_init_create_sheet

    session_mock.post.return_value = post_response_mock

    put_response_mock = MagicMock()
    put_response_mock.raise_for_status.return_value = None
    put_response_mock.json = categories_update_response

    session_mock.put.return_value = put_response_mock

    manager.session = session_mock

    with patch("budgetcli.data_manager.update_config") as mock_config:
        await manager.init()
        url = f"{manager.base_url}/:batchUpdate"
        data = {
            "requests": [{"addSheet": {"properties": {"title": "CATEGORIES"}}}]
        }
        session_mock.post.assert_called_once_with(url, json=data)
        session_mock.put.assert_called_once()
        mock_config.assert_called_once()


@pytest.mark.asyncio
async def test_update_method(manager, categories_update_response):
    """Test update method"""
    headers = ["CATEGORY"]

    response_mock = MagicMock()
    response_mock.raise_for_status.return_value = None
    response_mock.json = categories_update_response

    session_mock = AsyncMock()
    session_mock.put.return_value = response_mock

    manager.session = session_mock

    result = await manager.update(values=headers, a1="A1")
    params = "valueInputOption=USER_ENTERED"
    url = f"{manager.base_url}/values/CATEGORIES!A1?{params}"
    data = {
        "range": "CATEGORIES!A1",
        "majorDimension": "ROWS",
        "values": [["CATEGORY"]],
    }
    session_mock.put.assert_called_once_with(url, json=data)
    response_mock.raise_for_status.assert_called_once()
    assert result


@pytest.mark.asyncio
async def test_append_method(manager, categories_append_response):
    """Test update method"""
    values = ["Salary"]

    response_mock = MagicMock()
    response_mock.raise_for_status.return_value = None
    response_mock.json = categories_append_response

    session_mock = AsyncMock()
    session_mock.post.return_value = response_mock

    manager.session = session_mock

    result = await manager.append(values=values)
    params = "valueInputOption=USER_ENTERED"
    notation = "CATEGORIES!A2:A"
    url = f"{manager.base_url}/values/{notation}:append?{params}"
    data = {"majorDimension": "ROWS", "values": [["Salary"]]}
    session_mock.post.assert_called_once_with(url, json=data)
    response_mock.raise_for_status.assert_called_once()
    assert result


@pytest.mark.asyncio
async def test_get_records(manager, categories_list_response):
    """Test get transactions method"""

    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json = categories_list_response

    session_mock = AsyncMock()
    session_mock.get.return_value = mock_response

    manager.session = session_mock

    result = await manager.get_records()

    params = "majorDimension=ROWS"
    url = f"{manager.base_url}/values/CATEGORIES!A2:A101?{params}"
    session_mock.get.assert_called_once_with(url)
    mock_response.raise_for_status.assert_called_once()
    assert result
    assert len(result) == 4


@pytest.mark.asyncio
async def test_get_records_rows_option(manager, categories_rows_response):
    """Test get transactions with rows option"""

    response_mock = MagicMock()
    response_mock.raise_for_status.return_value = None
    response_mock.json = categories_rows_response

    session_mock = AsyncMock()
    session_mock.get.return_value = response_mock

    manager.session = session_mock

    result = await manager.get_records(rows=1)
    params = "majorDimension=ROWS"
    url = f"{manager.base_url}/values/CATEGORIES!A2:A2?{params}"
    session_mock.get.assert_called_once_with(url)
    response_mock.raise_for_status.assert_called_once()
    assert len(result) == 1

@pytest.mark.skip
@pytest.mark.asyncio
async def test_get_records_by_name(manager, categories_name_response):
    """Test get transactions for month"""

    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.text = categories_name_response

    session_mock = AsyncMock()
    session_mock.get.return_value = mock_response

    manager.session = session_mock

    with patch("budgetcli.data_manager.get_config") as mock_config:
        mock_config.return_value = "0"
        result = await manager.get_records_by_name(name="Salary")

        session_mock.get.assert_called_once()
        mock_response.raise_for_status.assert_called_once()
        assert result
