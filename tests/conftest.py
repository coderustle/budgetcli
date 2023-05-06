import json
from pathlib import Path

import pytest

FIXTURES_FOLDER = Path(__file__).parent / "fixtures"


@pytest.fixture
def transactions_list_response():
    file_path = FIXTURES_FOLDER / "list_transactions.json"
    with file_path.open("rb") as f:
        response = json.load(f)
        return response


@pytest.fixture
def transactions_month_response():
    file_path = FIXTURES_FOLDER / "query_month_transactions.txt"
    with file_path.open() as f:
        content = f.read()
        # read() appends an additional slash for \n
        to_replace = "/*O_o*/\\ngoogle.visualization.Query.setResponse("
        replaced = "/*O_o*/\ngoogle.visualization.Query.setResponse("
        return content.replace(to_replace, replaced)
