import asyncio
from typing import Any, TypeVar, Generic
from abc import ABC, abstractmethod

import httpx
from google.oauth2.credentials import Credentials

from .auth import load_user_token
from .utils.config import get_config
from .settings import API_URL

T = TypeVar("T", bound="AbstractDataManager")


class AbstractDataManager(ABC, Generic[T]):
    def __init__(self):
        self.spreadsheet_id = get_config("spreadsheet_id")
        self.base_url = f"{API_URL}/{self.spreadsheet_id}"
        self.session = httpx.AsyncClient()
        self.session.headers.update(self.get_auth_headers())

    @abstractmethod
    async def _append(self, row: list[str]) -> dict[str, str] | None:
        raise NotImplementedError

    @abstractmethod
    async def _list(self, range: str) -> dict[str, str] | None:
        raise NotImplementedError

    @staticmethod
    def get_auth_headers() -> dict:
        """Get the authentication headers from google credentials"""
        headers = {}
        credentials: Credentials | None = load_user_token()
        if credentials:
            credentials.apply(headers=headers)
        return headers


class TransactionDataManager(AbstractDataManager):
    TRANSACTIONS_RANGE = "TRANSACTIONS!A:E"

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

    async def _list(self, range: str) -> list[list[str]] | None:
        """List last 100 transactions"""
        params = "?majorDimension=ROWS"
        url = f"{self.base_url}/values/{range}{params}"
        response = await self.session.get(url)
        try:
            response.raise_for_status()
            result = response.json()
            return result.get("values", [])
        except httpx.HTTPStatusError as err:
            req_url = err.request.url
            status = err.response.status_code
            print(f"Error calling {req_url}, http status: {status}")

    def add_transaction(self, row: list) -> None:
        """Add a transaction to the spreadsheet"""
        asyncio.run(self._append(row=row, range=self.TRANSACTIONS_RANGE))

    def list_transactions(self) -> list[list[str]]:
        """List transactions. Default 100 rows"""
        result = asyncio.run(self._list(range=self.TRANSACTIONS_RANGE))
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
    async def create_sheet_for(title: str):
        """A class function to create a sheet in the spreadsheet"""
        session = httpx.AsyncClient()
        session.headers.update(AbstractDataManager.get_auth_headers())
        spreadsheet_id = get_config("spreadsheet_id")
        url = f"{API_URL}/{spreadsheet_id}:batchUpdate"
        body = {"requests": [{"addSheet": {"properties": {"title": title}}}]}
        response = await session.post(url, json=body)
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as err:
            req_url = err.request.url
            status = err.response.status_code
            print(f"Error calling {req_url}, http status: {status}")

    @staticmethod
    def create_manager_for(manager_name: str) -> Any | None:
        match manager_name:
            case "transactions":
                return TransactionDataManager()
            case "categories":
                pass
            case _:
                print("No manager found")
