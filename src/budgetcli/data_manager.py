from typing import Any, TypeVar, Generic
from abc import ABC, abstractmethod

import typer
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .auth import load_user_token
from .settings import API_SERVICE_NAME, API_VERSION
from .utils.config import get_config

T = TypeVar("T", bound="AbstractDataManager")

class AbstractDataManager(ABC, Generic[T]):
    def __init__(self):
        self.spreadsheet_id = get_config("spreadsheet_id")
        self.service = self.build_service()

    @abstractmethod
    def _init_headers(self, range: str, headers: list[str]) -> None:
        raise NotImplementedError

    @abstractmethod
    def _append(self, row: list[str]) -> dict[str, str] | None:
        raise NotImplementedError

    @abstractmethod
    def _list(self, rows: int = 100) -> dict[str, str] | None:
        raise NotImplementedError

    @staticmethod
    def build_service() -> Any:
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


class TransactionDataManager(AbstractDataManager):
    SHEET_NAME = "TRANSACTIONS"
    TRANSACTIONS_HEADER = "TRANSACTIONS!A1:F1"
    TRANSACTIONS_RANGE = "TRANSACTIONS!A2:F"

    def _init_headers(self, range: str, headers: list[str]) -> None:
        """Init tables in spreadsheet"""
        try:
            self.service.values().update(
                spreadsheetId=self.spreadsheet_id,
                valueInputOption="USER_ENTERED",
                range=range,
                body={"values": [headers]},
            ).execute()
        except HttpError as err:
            print(err)

    def _append(self, row: list[str]) -> dict[str, str] | None:
        """Append row to transactions sheet"""
        try:
            result = (
                self.service.values()
                .append(
                    spreadsheetId=self.spreadsheet_id,
                    valueInputOption="USER_ENTERED",
                    range=self.TRANSACTIONS_RANGE,
                    body={"values": [row]},
                )
                .execute()
            )
            return result
        except HttpError as err:
            print(err)

    def _list(self, rows: int = 100) -> dict[str, str] | None:
        """List last 100 transactions"""
        rows += 1
        range_name = f"{self.TRANSACTIONS_RANGE}{rows}"

        try:
            result: dict[str, str] = (
                self.service.values()
                .get(spreadsheetId=self.spreadsheet_id, range=range_name)
                .execute()
            )
            return result
        except HttpError as err:
            print(err)

    def init_transactions(self):
        """Init the spreadsheet"""
        transaction_headers = [
            "DATE",
            "CATEGORY",
            "DESCRIPTION",
            "INCOME",
            "OUTCOME",
        ]
        self._init_headers(self.TRANSACTIONS_HEADER, transaction_headers)

    def add_transaction(self, row: list) -> dict[str, str]:
        """Add a transaction to the spreadsheet"""
        result = self._append(row)
        if result:
            return result
        else:
            return {}

    def list_transactions(self, rows: int = 100) -> list[list[str]]:
        """List transactions. Default 100 rows"""
        result = self._list(rows)
        if result:
            values = result.get("values", [])
            check_rows = all(isinstance(row, list) for row in values)
            check_columns = all(
                isinstance(col, str) for rows in values for col in rows
            )
            if isinstance(values, list) and check_rows and check_columns:
                return values
        return []


class ManagerFactory:
    @staticmethod
    def create_manager_for(manager_name: str) -> Any | None:
        match manager_name:
            case "transactions":
                return TransactionDataManager()
            case "categories":
                pass
            case _:
                print("No manager found")
