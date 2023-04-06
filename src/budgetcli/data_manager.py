from typing import Any

import typer
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .auth import load_user_token
from .settings import API_SERVICE_NAME, API_VERSION
from .utils.config import get_config


class GoogleSheetManager:
    TRANSACTIONS_HEADER = "TRANSACTIONS!A1:F1"
    TRANSACTIONS_RANGE = "TRANSACTIONS!A2:F"

    def __init__(self, spradsheet_id: str, service: Any):
        self._spreadsheet_id = spradsheet_id
        self._service = service

    def init_sheets_headers(self):
        """Init the spreadsheet"""
        transaction_headers = [
            "ID",
            "DATE",
            "CATEGORY",
            "DESCRIPTION",
            "INCOME",
            "OUTCOME",
        ]
        self._init_table(self.TRANSACTIONS_HEADER, transaction_headers)

    def _init_table(self, range: str, headers: list[str]) -> None:
        """Init tables in spreadsheet"""
        if self._spreadsheet_id:
            self._service.values().update(
                spreadsheetId=self._spreadsheet_id,
                valueInputOption="USER_ENTERED",
                range=range,
                body={"values": [headers]},
            ).execute()

    def add_transaction(self, row: list) -> dict[str, str]:
        """Add a transaction to the spreadsheet"""
        result = {}
        if self._spreadsheet_id:
            result = (
                self._service.values()
                .append(
                    spreadsheetId=self._spreadsheet_id,
                    valueInputOption="USER_ENTERED",
                    range=self.TRANSACTIONS_RANGE,
                    body={"values": [row]},
                )
                .execute()
            )
            return result
        return result


def get_authenticated_service() -> Any:
    """Build the google service with provided credentials"""

    credentials: Credentials | None = load_user_token()

    if credentials:
        try:
            service = build(
                API_SERVICE_NAME, API_VERSION, credentials=credentials
            )

            return service.spreadsheets()

        except HttpError as error:
            print(error)
    else:
        print(":x: User is not authenticated")
        typer.Exit()


def get_data_manager() -> GoogleSheetManager | None:
    """Get the data manager"""
    service = get_authenticated_service()
    spreadsheet_id = get_config("spreadsheet_id")
    if spreadsheet_id:
        return GoogleSheetManager(spreadsheet_id, service)
