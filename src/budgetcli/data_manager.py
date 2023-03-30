from typing import Any

import typer
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .auth import load_user_token
from .settings import API_SERVICE_NAME, API_VERSION
from .utils import get_config


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


class GoogleSheetManager:
    TRANSACTIONS_RANGE = "TRANSACTIONS!A1"

    def __init__(self):
        self._sheet = get_authenticated_service()

    def init_sheets(self):
        """Init the spreadsheet"""
        values = ["ID", "DATE", "CATEGORY", "DESCRIPTION", "INCOME", "OUTCOME"]
        self._init_table("TRANSACTIONS!A1:E1", values)

    def _init_table(self, range: str, headers: list[str]) -> dict | None:
        """Init tables in spreadsheet"""
        spreadsheet_id = get_config("spreadsheet_id")
        if spreadsheet_id:
            result = (
                self._sheet.values()
                .update(
                    spreadsheetId=spreadsheet_id,
                    valueInputOption="USER_ENTERED",
                    range=range,
                    body={"values": [headers]},
                )
                .execute()
            )
            return result
