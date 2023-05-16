import asyncio
import json
from abc import ABC, abstractmethod
from typing import Coroutine, Generic, TypeVar

import httpx
from rich.pretty import pprint

from .auth import get_auth_headers
from .settings import API_URL, GVI_URL
from .utils.config import get_config

T = TypeVar("T", bound="AbstractDataManager")

SPREADSHEET_ID = get_config("spreadsheet_id")


class Client(httpx.AsyncClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.headers.update(get_auth_headers())
        self.timeout = 30.0  # default timeout


class AbstractDataManager(ABC, Generic[T]):
    """
    Abstract class for data managers
    """

    def __init__(self, session: Client):
        self.session = session
        self.base_url = f"{API_URL}/{SPREADSHEET_ID}"
        self.gvi_url = f"{GVI_URL}/{SPREADSHEET_ID}/gviz/tq"

    @abstractmethod
    async def init(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, values: list[str], a1: str) -> dict[str, str]:
        raise NotImplementedError

    @abstractmethod
    async def append(self, values: list[str]) -> dict[str, str]:
        raise NotImplementedError

    @abstractmethod
    async def get_records(self, rows: int = 100):
        raise NotImplementedError

    async def _update(
        self,
        values: list[str],
        a1: str,
    ) -> dict[str, str]:
        """Update a row or a specific cell"""
        params = "valueInputOption=USER_ENTERED"
        url = f"{self.base_url}/values/{a1}?{params}"
        body = {"range": a1, "majorDimension": "ROWS", "values": [values]}
        response = await self.session.put(url, json=body)
        try:
            response.raise_for_status()
            data = response.json()
            return data
        except httpx.HTTPStatusError as err:
            req_url = err.request.url
            status = err.response.status_code
            pprint(f"Error calling {req_url}, http status: {status}")
        return {}

    async def _append(self, values: list[str], a1: str) -> dict[str, str]:
        """Append row to sheet"""
        params = "valueInputOption=USER_ENTERED"
        url = f"{self.base_url}/values/{a1}:append?{params}"
        body = {"majorDimension": "ROWS", "values": [values]}
        response = await self.session.post(url, json=body)
        try:
            response.raise_for_status()
            data = response.json()
            return data
        except httpx.HTTPStatusError as err:
            req_url = err.request.url
            status = err.response.status_code
            pprint(f"Error calling {req_url}, http status: {status}")
        return {}

    async def _list(self, a1: str) -> list[list[str]] | None:
        """List data from a given range"""
        params = "?majorDimension=ROWS"
        url = f"{self.base_url}/values/{a1}{params}"
        response = await self.session.get(url)
        try:
            response.raise_for_status()
            result = response.json()
            return result.get("values", [])
        except httpx.HTTPStatusError as err:
            req_url = err.request.url
            status = err.response.status_code
            pprint(f"Error calling {req_url}, http status: {status}")
        return None

    async def _query(
        self, query: str, sheet: str
    ) -> list[dict[str, list]] | None:
        """A method to use Google Visualization API"""
        params = f"sheet={sheet}&tq={query}&tqx=out:json"
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
        return None

    async def _get_sheet(self, title: str) -> dict[str, str] | None:
        """Check if the sheet with the given title exists"""
        params = "fields=sheets.properties"
        url = f"{self.base_url}?{params}"
        response = await self.session.get(url)
        try:
            response.raise_for_status()
            data = response.json()
            sheets = data.get("sheets")
            if sheets:
                for sheet in sheets:
                    if sheet["properties"]["title"] == title:
                        return sheet["properties"]
        except httpx.HTTPStatusError as err:
            req_url = err.request.url
            status = err.response.status_code
            pprint(f"Error calling {req_url}, http status: {status}")
        return None

    async def _create_sheet(self, title: str) -> dict[str, str] | None:
        """Create sheet with the given title and returns its properties"""
        url = f"{self.base_url}/:batchUpdate"
        body = {"requests": [{"addSheet": {"properties": {"title": title}}}]}
        response = await self.session.post(url, json=body)
        try:
            response.raise_for_status()
            data = response.json()
            replies = data.get("replies", [])
            sheet = replies[0].get("addSheet")
            properties = sheet.get("properties")
            return properties
        except httpx.HTTPStatusError as err:
            req_url = err.request.url
            status = err.response.status_code
            pprint(f"Error calling {req_url}, http status: {status}")
        return None

    async def _get_sheet_or_create(self, sheet_name: str) -> dict[str, str]:
        """Get sheet or create if not exists"""
        sheet: Coroutine = self._get_sheet(sheet_name)
        try:
            properties = await asyncio.wait_for(sheet, timeout=5)
            if properties:
                return properties
            else:
                create: Coroutine = self._create_sheet(sheet_name)
                properties = await asyncio.wait_for(create, timeout=5)
                if properties:
                    return properties
        except asyncio.TimeoutError:
            pass
        return {}

    @staticmethod
    def _process_row(row: dict[str, list]) -> list[str]:
        """Helper function to process transaction rows"""
        records = []
        for cel in row.get("c", []):
            if cel and "Date(" in str(cel.get("v")):
                date = cel.get("f")
                records.append(date)
            elif cel:
                records.append(cel.get("v"))
            else:
                records.append("")
        return records


class TransactionDataManager(AbstractDataManager):
    SHEET_NAME = "TRANSACTIONS"
    FIRST_COL = "A"
    LAST_COL = "E"
    ROW_START = 2
    RANGE = f"{SHEET_NAME}!{FIRST_COL}{ROW_START}:{LAST_COL}"
    HEADERS = ["DATE", "CATEGORY", "DESCRIPTION", "INCOME", "OUTCOME"]

    async def init(self) -> None:
        """Create TRANSACTIONS sheet if not exists"""
        a1 = f"{self.SHEET_NAME}!A1"
        headers = "DATE CATEGORY DESCRIPTION INCOME OUTCOME MONTH YEAR"
        sheet_coroutine: Coroutine = self._get_sheet_or_create(self.SHEET_NAME)
        update_coroutine: Coroutine = self._update(headers.split(), a1)
        try:
            sheet = await asyncio.wait_for(sheet_coroutine, timeout=30.0)
            if sheet:
                await asyncio.wait_for(update_coroutine, timeout=30.0)
        except asyncio.TimeoutError:
            print("Timeout error")

    async def update(self, values: list[str], a1: str) -> dict[str, str]:
        notation = f"{self.SHEET_NAME}!{a1}"
        result = await self._update(values=values, a1=notation)
        return result

    async def append(self, values: list) -> dict[str, str]:
        """Add a transaction to the spreadsheet"""
        result = await self._append(values=values, a1=self.RANGE)
        return result

    async def get_records(self, rows: int = 100) -> list[list[str]]:
        """List transactions. Default 100 rows"""
        transaction_range = f"{self.RANGE}{rows + 1}"
        result: list[list[str]] = await self._list(a1=transaction_range)
        return result if result else []

    async def get_records_for_month(self, month: int) -> list[list[str]]:
        """Query the transactions for current month"""
        month -= 1  # month query starts from 0 to 11
        query = f"select A,B,C,D,E where month(A)={month}"
        rows = await self._query(query, self.SHEET_NAME)
        transactions = [self._process_row(i) for i in rows] if rows else []
        return transactions


class CategoryDataManager(AbstractDataManager):
    SHEET_NAME = "CATEGORIES"
    FIRST_COL = "A"
    LAST_COL = "A"
    ROW_START = 2
    RANGE = f"{SHEET_NAME}!{FIRST_COL}{ROW_START}:{LAST_COL}"

    async def init(self) -> None:
        """Create CATEGORY sheet if not exists"""
        a1 = f"{self.SHEET_NAME}!A1"
        headers = "CATEGORY"
        sheet_coroutine: Coroutine = self._get_sheet_or_create(self.SHEET_NAME)
        update_coroutine: Coroutine = self._update([headers], a1)
        try:
            sheet = await asyncio.wait_for(sheet_coroutine, timeout=30.0)
            if sheet:
                await asyncio.wait_for(update_coroutine, timeout=30.0)
        except asyncio.TimeoutError:
            print("Timeout error")

    async def update(self, values: list[str], a1: str) -> dict[str, str]:
        notation = f"{self.SHEET_NAME}!{a1}"
        result = await self._update(values=values, a1=notation)
        return result

    async def append(self, values: list) -> dict[str, str]:
        """Add new category in Google sheet"""
        result = await self._append(values=values, a1=self.RANGE)
        return result

    async def get_records(self, rows: int = 100):
        """Return all categories"""
        category_range = f"{self.RANGE}{rows + 1}"
        result: list[list[str]] = await self._list(a1=category_range)
        return result if result else []

    async def get_records_by_name(self, name: str) -> list[list[str]]:
        """Return a category by a given name"""
        name = name.lower()
        query = f"select A where A='{name}'"
        rows = await self._query(query, self.SHEET_NAME)
        categories = [self._process_row(i) for i in rows] if rows else []
        return categories


class BudgetDataManager(AbstractDataManager):
    SHEET_NAME = "BUDGET"
    FIRST_COL = "A"
    LAST_COL = "F"
    ROW_START = 2
    RANGE = f"{SHEET_NAME}!{FIRST_COL}{ROW_START}:{LAST_COL}"

    async def init(self) -> None:
        a1 = f"{self.SHEET_NAME}!A1"
        headers = "DATE CATEGORY PLANNED SPENT"
        sheet_coroutine = self._get_sheet_or_create(self.SHEET_NAME)
        update_coroutine = self._update(headers.split(), a1)
        try:
            sheet = await asyncio.wait_for(sheet_coroutine, timeout=30.0)
            if sheet:
                await asyncio.wait_for(update_coroutine, timeout=30.0)
        except asyncio.TimeoutError:
            print("Timeout error")

    async def update(self, values: list[str], a1: str) -> dict[str, str]:
        notation = f"{self.SHEET_NAME}!{a1}"
        result = await self._update(values=values, a1=notation)
        return result

    async def append(self, values: list[str]) -> dict[str, str]:
        result = await self._append(values=values, a1=self.RANGE)
        return result

    async def get_records(self, rows: int = 100):
        budget_range = f"{self.RANGE}{rows + 1}"
        result: list[list[str]] = await self._list(a1=budget_range)
        return result if result else []

    async def get_records_by_month(self, month: int) -> list[list[str]]:
        month -= 1  # month query starts from 0
        query = f"select A,B,C,D where month(A)={month}"
        rows = await self._query(query, self.SHEET_NAME)
        budgets = [self._process_row(i) for i in rows] if rows else []
        return budgets

    async def get_records_by_month_and_category(
        self, month: int, cat: str
    ) -> list[list[str]]:
        month -= 1  # month array starts from 0
        query = f"select A,B,C,D where month(A)={month} and B contains '{cat}'"
        rows = await self._query(query, self.SHEET_NAME)
        budgets = [self._process_row(i) for i in rows] if rows else []
        return budgets
