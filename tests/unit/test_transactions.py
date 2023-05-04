import pytest
from budgetcli.data_manager import ManagerFactory


@pytest.fixture
def manager():
    return ManagerFactory.create_manager_for("transactions")


@pytest.mark.slow
@pytest.mark.asyncio
async def test_init_sheet(manager, capsys):
    """Test init sheet method"""
    await manager.init()
    output = capsys.readouterr()
    text = "✔ transactions_sheet_index was updated"
    assert text in output.out
