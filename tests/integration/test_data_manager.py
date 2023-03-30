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


def test_init_sheet_tables():
    """Test init_sheet_tables method"""

    sheet_manager = GoogleSheetManager()
    sheet_manager.init_sheet_tables()
