from unittest.mock import patch

from budgetcli.data_manager import GoogleSheetManager, get_authenticated_service


def test_authenticated_service():
    """Test authenticated services"""

    service = get_authenticated_service()

    assert service is not None


def test_authenticated_service_with_wrong_credentials():
    """Test with wrong credentials or when token.json is missing"""

    to_patch = "budgetcli.data_manager.load_user_token"

    with patch(to_patch, return_value=None, autospec=True):
        service = get_authenticated_service()

        assert service is None


def test_google_sheet_manager_instance():
    """Test instance of the GoogleSheetManager"""

    sheet_manager = GoogleSheetManager()

    assert sheet_manager is not None
    assert isinstance(sheet_manager, GoogleSheetManager)


def test_init_tables():
    """Test init_sheet_tables method"""

    values = ["ID", "DATE", "CATEGORY", "DESCRIPTION", "AMOUNT"]
    range = "TRANSACTIONS!A1:E1"

    sheet_manager = GoogleSheetManager()
    result = sheet_manager._init_table(range=range, headers=values)

    assert result is not None
