import asyncio
from abc import ABC, abstractmethod

from rich import print

from .models import Transaction
from .settings import CURRENCY
from .data_manager import ManagerFactory
from .utils.display import get_transaction_table, task_progress


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError


class InitTransactionCommand(Command):
    def __init__(self):
        self.manager = ManagerFactory.create_manager_for("transactions")

    def execute(self):
        if self.manager is not None:
            with task_progress(description="Processing.."):
                asyncio.run(self.manager.init_sheet())
                print(":heavy_check_mark: Init was completed successfully")


class AddTransactionCommand(Command):
    def __init__(self, transaction: Transaction):
        self.transaction = transaction
        self.manager = ManagerFactory.create_manager_for("transactions")

    def execute(self):
        if self.manager is not None:
            with task_progress(description="Processing.."):
                row = self.transaction.to_sheet_row()
                asyncio.run(self.manager.add_transaction(row))
                print(":heavy_check_mark: Transaction was added successfully")


class ListTransactionCommand(Command):
    def __init__(self, rows: int, month: int | None):
        self.rows = rows
        self.month = month
        self.manager = ManagerFactory.create_manager_for("transactions")

    def execute(self):
        table = get_transaction_table()
        if self.manager is not None:
            with task_progress(description="Processing.."):
                transactions = []
                if self.month:
                    transactions = asyncio.run(
                        self.manager.get_transactions_for_month(self.month)
                    )
                else:
                    transactions = asyncio.run(
                        self.manager.list_transactions(self.rows)
                    )
                for row in transactions:
                    income = f"{CURRENCY} {row[3]}"
                    outcome = f"{CURRENCY} {row[4]}"
                    table.add_row(row[0], row[1], row[2], income, outcome)
        print(table)
