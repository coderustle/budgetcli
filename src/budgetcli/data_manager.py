import asyncio
from typing import Any, TypeVar, Generic
from abc import ABC, abstractmethod

import httpx
from google.oauth2.credentials import Credentials
from rich.pretty import pprint

from .auth import load_user_token
from .settings import API_URL
from .utils.config import get_config

T = TypeVar("T", bound="AbstractDataManager")

SPREADSHEET_ID = get_config("spreadsheet_id")


class AbstractDataManager(ABC, Generic[T]):
    def __init__(self):
        self.base_url = f"{API_URL}/{SPREADSHEET_ID}"
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

    async def sheet_exists(self, title: str) -> bool:
        """Check if the sheet with the given title exists"""
        params = "fields=sheets.properties.title"
        url = f"{self.base_url}?{params}"
        response = await self.session.get(url)
        try:
            response.raise_for_status()
            data = response.json()
            sheets = data.get("sheets")
            for sheet in sheets:
                if sheet["properties"]["title"] == title:
                    return True
        except httpx.HTTPStatusError as err:
            req_url = err.request.url
            status = err.response.status_code
            pprint(f"Error calling {req_url}, http status: {status}")
        return False

    async def create_sheet(self, title: str) -> bool:
        """Create sheet with the given title"""
        url = f"{self.base_url}/:batchUpdate"
        body = {"requests": [{"addSheet": {"properties": {"title": title}}}]}
        response = await self.session.post(url, json=body)
        try:
            response.raise_for_status()
            return True
        except httpx.HTTPStatusError as err:
            req_url = err.request.url
            status = err.response.status_code
            pprint(f"Error calling {req_url}, http status: {status}")
        return False


class TransactionDataManager(AbstractDataManager):
    TRANSACTIONS_RANGE = "TRANSACTIONS!A:E"

    async def _append(self, row: list[str], range: str) -> None:
        """Append row to transactions sheet"""
        params = "valueInputOption=USER_ENTERED"
        url = f"{self.base_url}/values/{range}:append?{params}"
        body = {"majorDimension": "ROWS", "values": [row]}
        response = await self.session.post(url, json=body)

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as err:
            req_url = err.request.url
            status = err.response.status_code
            pprint(f"Error calling {req_url}, http status: {status}")

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
            pprint(f"Error calling {req_url}, http status: {status}")

    async def init_sheet(self):
        """Create TRANSACTIONS sheet if not exists"""
        check_task = asyncio.create_task(self.sheet_exists("TRANSACTIONS"))
        create_task = asyncio.create_task(self.create_sheet("TRANSACTIONS"))
        sheet = await check_task
        if not sheet:
            await create_task


    async def add_transaction(self, row: list) -> None:
        """Add a transaction to the spreadsheet"""
        task = asyncio.create_task(self._append(row=row, range=self.TRANSACTIONS_RANGE))
        await task

    async def list_transactions(self) -> list[list[str]]:
        """List transactions. Default 100 rows"""
        task = asyncio.create_task(self._list(range=self.TRANSACTIONS_RANGE))
        result = await task
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
                pprint("No manager found")
