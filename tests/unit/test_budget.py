from unittest.mock import AsyncMock, MagicMock

import pytest

from budgetcli.data_manager import ManagerFactory


@pytest.fixture()
def manager():
    return ManagerFactory.create_manager_for("budgets")


@pytest.mark.asyncio
async def test_init_sheet_exists(
    manager, init_get_sheet, budget_update_response
):
    """Test init sheet get sheet"""
    session_mock = AsyncMock()

    get_response_mock = MagicMock()
    get_response_mock.raise_for_status.return_value = None
    get_response_mock.json = init_get_sheet

    session_mock.get.return_value = get_response_mock

    put_response_mock = MagicMock()
    put_response_mock.raise_for_status.return_value = None
    put_response_mock.json = budget_update_response

    session_mock.put.return_value = put_response_mock

    manager.session = session_mock

    await manager.init()

    session_mock.get.assert_called_once()
    session_mock.put.assert_called_once()
    get_response_mock.raise_for_status.assert_called_once()
