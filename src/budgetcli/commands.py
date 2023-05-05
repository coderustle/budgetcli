import asyncio
from abc import ABC, abstractmethod

from rich import print

from .data_manager import ManagerFactory
from .models import Transaction, Category
from .settings import CURRENCY
from .utils.display import (
    get_transaction_table,
    task_progress,
    get_category_table,
)


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError


class InitCommand(Command):
    def __init__(self):
        self.tra_manager = ManagerFactory.create_manager_for("transactions")
        self.cat_manager = ManagerFactory.create_manager_for("categories")

    async def init(self) -> None:
        try:
            cat_task = asyncio.create_task(self.cat_manager.init())
            tra_task = asyncio.create_task(self.tra_manager.init())
            with task_progress(description="Processing.."):
                await cat_task
                await tra_task
                print(":heavy_check_mark: Init was completed successfully")
        except AttributeError:
            print("Init factory manager error")

    def execute(self) -> None:
        asyncio.run(self.init())


class AddTransactionCommand(Command):
    def __init__(self, transaction: Transaction):
        self.transaction = transaction
        self.manager = ManagerFactory.create_manager_for("transactions")

    def execute(self):
        try:
            with task_progress(description="Processing.."):
                row = self.transaction.to_sheet_row()
                asyncio.run(self.manager.append(row))
                print(":heavy_check_mark: Transaction was added successfully")
            pass
        except AttributeError:
            print("Init factory manager error")


class ListTransactionCommand(Command):
    """Command to list transactions"""

    def __init__(self, rows: int, month: int | None):
        self.rows = rows
        self.month = month
        self.manager = ManagerFactory.create_manager_for("transactions")

    def execute(self):
        table = get_transaction_table()
        if self.manager is not None:
            with task_progress(description="Processing.."):
                if self.month:
                    transactions = asyncio.run(
                        self.manager.get_records_for_month(self.month)
                    )
                else:
                    transactions = asyncio.run(
                        self.manager.get_records(self.rows)
                    )
                for row in transactions:
                    income = f"{CURRENCY} {row[3]}"
                    outcome = f"{CURRENCY} {row[4]}"
                    table.add_row(row[0], row[1], row[2], income, outcome)
        print(table)


class AddCategoryCommand(Command):
    def __init__(self, category: Category):
        self.category = category
        self.manager = ManagerFactory.create_manager_for("categories")

    def execute(self) -> None:
        try:
            with task_progress(description="Processing.."):
                row = self.category.to_sheet_row()
                asyncio.run(self.manager.append(row))
                print(":heavy_check_mark: Category was added successfully")
        except AttributeError:
            print("Init factory manager error")


class ListCategoryCommand(Command):
    def __init__(self, rows: int):
        self.rows = rows
        self.manager = ManagerFactory.create_manager_for("categories")

    def execute(self) -> None:
        table = get_category_table()
        try:
            with task_progress(description="Processing"):
                if self.rows:
                    categories = asyncio.run(
                        self.manager.get_records(rows=self.rows)
                    )
                    for row in categories:
                        table.add_row(row[0])
        except AttributeError:
            print("Init factory manager error")
        print(table)
