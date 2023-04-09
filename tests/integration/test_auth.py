from unittest.mock import patch

from budgetcli.data_manager import AbstractDataManager


def test_authenticated_service():
    """Test authenticated services"""
    service = AbstractDataManager.build_service()
    assert service is not None


def test_authenticated_service_with_wrong_credentials():
    """Test with wrong credentials or when token.json is missing"""
    to_patch = "budgetcli.data_manager.load_user_token"
    with patch(to_patch, return_value=None, autospec=True):
        service = AbstractDataManager.build_service()
        assert service is None
