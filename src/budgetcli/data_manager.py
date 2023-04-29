import asyncio
import json
from typing import Any, TypeVar, Generic
from abc import ABC
from rich.pretty import pprint

import httpx
from google.oauth2.credentials import Credentials

from .auth import load_user_token
from .settings import API_URL, GVI_URL
from .utils.config import get_config, update_config

T = TypeVar("T", bound="AbstractDataManager")

SPREADSHEET_ID = get_config("spreadsheet_id")


class AbstractDataManager(ABC, Generic[T]):
    def __init__(self):
        self.base_url = f"{API_URL}/{SPREADSHEET_ID}"
        self.gvi_url = f"{GVI_URL}/{SPREADSHEET_ID}/gviz/tq"
        self.session = httpx.AsyncClient()
        self.session.headers.update(self.get_auth_headers())

    async def _append(
        self, row: list[str], range: str
    ) -> dict[str, str] | None:
        """Append row to sheet"""
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

    async def _list(self, range: str) -> dict[str, str] | None:
        """List data from a given range"""
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

    async def _query(self, query: str, sheet_index: int) -> list[dict[str, list]] | None:
        """A method to use Goolge Visualization API"""
        params = f"gid={sheet_index}&tq={query}&tqx=out:json"
        url = f"{self.gvi_url}?{params}"
        response = await self.session.get(url)
        try:
            response.raise_for_status()
            to_replace = "/*O_o*/\ngoogle.visualization.Query.setResponse("
            clean_data = response.text.replace(to_replace, "")[:-2]
            json_data = json.loads(clean_data)
            rows = json_data.get("table", {}).get("rows", [])
            return rows
        except httpx.HTTPStatusError as err:
            req_url = err.request.url
            status = err.response.status_code
            pprint(f"Error calling {req_url}, http status: {status}")

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

    async def get_sheet_index(self, title: str) -> int:
        """Get google sheet index position"""
        params = "fields=sheets"
        url = f"{self.base_url}?{params}"
        response = await self.session.get(url)
        try:
            response.raise_for_status()
            data = response.json()
            sheets = data.get("sheets")
            for sheet in sheets:
                if sheet["properties"]["title"] == title:
                    sheet_index = sheet["properties"]["index"]
                    return sheet_index
        except httpx.HTTPStatusError as err:
            req_url = err.request.url
            status = err.response.status_code
            pprint(f"Error calling {req_url}, http status: {status}")
        return -1

    async def create_sheet(self, title: str) -> dict[str, str] | None:
        """Create sheet with the given title"""
        url = f"{self.base_url}/:batchUpdate"
        body = {"requests": [{"addSheet": {"properties": {"title": title}}}]}
        response = await self.session.post(url, json=body)
        try:
            response.raise_for_status()
            data = response.json()
            replies = data.get('replies', []) 
            sheet = replies[0].get("addSheet")
            properties = sheet.get("properties")
            return properties
        except httpx.HTTPStatusError as err:
            req_url = err.request.url
            status = err.response.status_code
            pprint(f"Error calling {req_url}, http status: {status}")


class TransactionDataManager(AbstractDataManager):
    SHEET_NAME = "TRANSACTIONS!"
    FIRST_COLUMN = "A"
    LAST_COLUMN = "E"
    TRANSACTIONS_RANGE = f"{SHEET_NAME}{FIRST_COLUMN}1:{LAST_COLUMN}"

    async def init_sheet(self):
        """Create TRANSACTIONS sheet if not exists"""
        check = self.sheet_exists("TRANSACTIONS")
        index = self.get_sheet_index("TRANSACTIONS")
        try:
            exists = await asyncio.wait_for(check, timeout=5)
            if exists:
                index = await asyncio.wait_for(index, timeout=5)
                update_config("transactions_sheet_index", str(index))
            else:
                create = self.create_sheet("TRANSACTIONS")
                properties = await asyncio.wait_for(create, timeout=5)
                if properties:
                    index =  properties.get("index")
                    update_config("transactions_sheet_index", str(index))
        except asyncio.TimeoutError:
            print("Timeout error")

    async def get_transactions_for_month(
        self, month: int 
    ) -> list[list[str]] | None:
        """Query the transactions for current month"""
        month = month - 1  # month query starts from 0 to 11
        query = f"select A,B,C,D,E where month(A)={month}"
        transactions = []
        sheet_index = get_config("transactions_sheet_index")
        rows = None
        if sheet_index:
            index = int(sheet_index)
            rows = await self._query(query, index)
        else:
            rows = await self._query(query, 0)
        if rows:
            for row in rows:
                transaction = []
                for cel in row.get("c", []):
                    if "Date(" in str(cel.get("v")):
                        date = cel.get("f")
                        transaction.append(date)
                    else:
                        transaction.append(cel.get("v"))
                transactions.append(transaction)
        return transactions

    async def add_transaction(self, row: list) -> None:
        """Add a transaction to the spreadsheet"""
        await self._append(row=row, range=self.TRANSACTIONS_RANGE)

    async def list_transactions(self, rows: int = 100) -> list[list[str]]:
        """List transactions. Default 100 rows"""
        transaction_range = f"{self.TRANSACTIONS_RANGE}{rows}"
        result = await self._list(range=transaction_range)
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
