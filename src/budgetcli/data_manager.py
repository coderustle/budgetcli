from typing import Any

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials

import typer

from .settings import API_VERSION, API_SERVICE_NAME
from .auth import load_user_token
from .utils import get_config


def get_authenticated_service() -> Any:
    """Build the google service with provided credentials"""

    credentials: Credentials | None = load_user_token()

    if credentials:
        try:
            service = build(API_SERVICE_NAME, API_VERSION, credentials)

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
            result = self._sheet().values().get(
                    spreadsheetId=spreadsheet_id,
                    range=self.CATEGORIES_RANGE,
                    ).execute()
            print(result)
        
