import asyncio
from typing import Any, TypeVar, Generic
from abc import ABC, abstractmethod

import httpx
import typer
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .auth import load_user_token
from .settings import API_SERVICE_NAME, API_VERSION
from .utils.config import get_config

T = TypeVar("T", bound="AbstractDataManager")


class AbstractDataManager(ABC, Generic[T]):
    API_URL = "https://sheets.googleapis.com/v4/spreadsheets"

    def __init__(self):
        self.spreadsheet_id = get_config("spreadsheet_id")
        self.service = self.build_service()
        self.base_url = f"{self.API_URL}/{self.spreadsheet_id}"
        self.session = httpx.AsyncClient()
        self.session.headers.update(self.get_auth_headers())

    @abstractmethod
    async def _init_headers(self, range: str, headers: list[str]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def _init_sheet(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def _append(self, row: list[str]) -> dict[str, str] | None:
        raise NotImplementedError

    @abstractmethod
    async def _list(self, rows: int = 100) -> dict[str, str] | None:
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

    @staticmethod
    def get_auth_headers() -> dict:
        """Get the authentication headers from google credentials"""
        headers = {}
        credentials: Credentials | None = load_user_token()
        if credentials:
            credentials.apply(headers=headers)
        return headers


class TransactionDataManager(AbstractDataManager):
    SHEET_NAME = "TRANSACTIONS"
    TRANSACTIONS_HEADER = "TRANSACTIONS!A1:E1"
    TRANSACTIONS_RANGE = "TRANSACTIONS!A2:E"

    async def _init_sheet(self) -> None:
        """Create sheet TRANSACTIONS if not exists"""
        ...

    async def _init_headers(self, range: str, headers: list[str]) -> None:
        """Init tables in spreadsheet"""
        params = "?valueInputOption=USER_ENTERED"
        url = f"{self.base_url}/values/{range}{params}"
        body = {"majorDimension": "ROWS", "values": [headers]}
        response = await self.session.put(url, json=body)
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as err:
            request = err.request.url
            status = err.response.status_code
            print(f"Error calling {request}, http status: {status}")

    async def _append(self, row: list[str], range: str) -> None:
        """Append row to transactions sheet"""
        params = "?valueInputOption=USER_ENTERED"
        url = f"{self.base_url}/values/{range}:append{params}"
        body = {"majorDimension": "ROWS", "values": [row]}
        response = await self.session.post(url, json=body)

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as err:
            req_url = err.request.url
            status = err.response.status_code
            print(f"Error calling {req_url}, http status: {status}")

    async def _list(self, rows: int = 100) -> list[list[str]] | None:
        """List last 100 transactions"""
        rows += 1
        range_name = f"{self.TRANSACTIONS_RANGE}{rows}"
        params = "?majorDimension=ROWS"
        url = f"{self.base_url}/values/{range_name}{params}"
        response = await self.session.get(url)
        try:
            response.raise_for_status()
            result = response.json()
            return result.get("values", [])
        except httpx.HTTPStatusError as err:
            req_url = err.request.url
            status = err.response.status_code
            print(f"Error calling {req_url}, http status: {status}")

    def init_transactions(self):
        """Init the spreadsheet"""
        headers = ["DATE", "CATEGORY", "DESCRIPTION", "INCOME", "OUTCOME"]
        asyncio.run(self._init_headers(self.TRANSACTIONS_HEADER, headers))

    def add_transaction(self, row: list) -> None:
        """Add a transaction to the spreadsheet"""
        asyncio.run(self._append(row=row, range=self.TRANSACTIONS_RANGE))

    def list_transactions(self, rows: int = 100) -> list[list[str]]:
        """List transactions. Default 100 rows"""
        result = asyncio.run(self._list(rows=rows))
        if result:
            check_rows = all(isinstance(row, list) for row in result)
            check_columns = all(
                isinstance(col, str) for rows in result for col in rows
            )
            if isinstance(result, list) and check_rows and check_columns:
                return result
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
