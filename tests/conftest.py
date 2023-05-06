import json
from pathlib import Path

import pytest

FIXTURES_FOLDER = Path(__file__).parent / "fixtures"


@pytest.fixture
def transactions_init_get_sheet():
    file_path = FIXTURES_FOLDER / "get_transactions_sheet.json"

    def json_response():
        with file_path.open("rb") as f:
            response = json.load(f)
            return response

    return json_response


@pytest.fixture
def transactions_update_response():
    file_path = FIXTURES_FOLDER / "update_transactions.json"

    def json_response():
        with file_path.open("rb") as f:
            response = json.load(f)
            return response

    return json_response


@pytest.fixture
def transactions_list_response():
    file_path = FIXTURES_FOLDER / "list_transactions.json"

    def json_response():
        with file_path.open("rb") as f:
            response = json.load(f)
            return response

    return json_response


@pytest.fixture
def transactions_rows_response():
    file_path = FIXTURES_FOLDER / "one_transaction.json"

    def json_response():
        with file_path.open("rb") as f:
            response = json.load(f)
            return response

    return json_response


@pytest.fixture
def transactions_month_response():
    file_path = FIXTURES_FOLDER / "query_month_transactions.txt"
    with file_path.open() as f:
        content = f.read()
        # read() appends an additional slash for \n
        to_replace = "/*O_o*/\\ngoogle.visualization.Query.setResponse("
        replaced = "/*O_o*/\ngoogle.visualization.Query.setResponse("
        return content.replace(to_replace, replaced)
