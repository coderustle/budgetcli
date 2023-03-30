from typing import Any

import typer
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from rich.pretty import pprint

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
    CATEGORIES_RANGE = "CATEGORIES!A1"

    def __init__(self):
        self._sheet = get_authenticated_service()

    def init_sheet_tables(self):
        """Init tables in spreadsheet"""
        spreadsheet_id = get_config("spreadsheet_id")
        if spreadsheet_id:
            print(spreadsheet_id)
            print(self._sheet)
            result = (
                self._sheet.values()
                .get(
                    spreadsheetId=spreadsheet_id,
                    range=self.CATEGORIES_RANGE,
                )
                .execute()
            )
            pprint(result, expand_all=True)
