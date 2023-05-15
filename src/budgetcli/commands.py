import asyncio
from abc import ABC, abstractmethod

from rich import print

from .data_manager import ManagerFactory
from .models import Transaction, Category, Budget
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
        self.bud_manager = ManagerFactory.create_manager_for("budgets")

    async def init(self) -> None:
        try:
            tasks = [
                self.tra_manager.init(),
                self.cat_manager.init(),
                self.bud_manager.init(),
            ]
            with task_progress(description="Processing.."):
                await asyncio.gather(*tasks)
                print(":heavy_check_mark: Init was completed successfully")
        except AttributeError:
            print("Init factory manager error")

    def execute(self) -> None:
        asyncio.run(self.init())


class AddTransactionCommand(Command):
    def __init__(self, transaction: Transaction):
        self.transaction = transaction
        self.tra_manager = ManagerFactory.create_manager_for("transactions")
        self.cat_manager = ManagerFactory.create_manager_for("categories")

    async def add_transaction(self):
        tra_row = self.transaction.to_sheet_row()
        category_name = self.transaction.category

        categories = await self.cat_manager.get_records_by_name(category_name)
        if categories and category_name in categories[0]:
            await self.tra_manager.append(tra_row)
        else:
            category = Category(name=category_name)
            row = category.to_sheet_row()
            tasks = [self.cat_manager.append(row), self.tra_manager(tra_row)]
            await asyncio.gather(*tasks)

    def execute(self):
        try:
            with task_progress(description="Processing.."):
                asyncio.run(self.add_transaction())
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
                    get = self.manager.get_records_for_month(self.month)
                    transactions = asyncio.run(get)
                else:
                    get = self.manager.get_records(self.rows)
                    transactions = asyncio.run(get)
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
    def __init__(self, rows: int, name: str):
        self.rows = rows
        self.name = name
        self.manager = ManagerFactory.create_manager_for("categories")

    def execute(self) -> None:
        table = get_category_table()
        try:
            with task_progress(description="Processing"):
                if self.name:
                    get = self.manager.get_records_by_name(name=self.name)
                    categories = asyncio.run(get)
                else:
                    get = self.manager.get_records(rows=self.rows)
                    categories = asyncio.run(get)
                for row in categories:
                    table.add_row(row[0])
        except AttributeError:
            print("Init factory manager error")
        print(table)


class AddBudgetCommand(Command):
    def __init__(self, budget: Budget):
        self.budget = budget
        self.bud_manager = ManagerFactory.create_manager_for("budgets")

    async def add_budget(self):
        row = self.budget.to_sheet_row()
        cat = self.budget.category
        month = self.budget.date.month
        rows = await self.bud_manager.get_records_by_month_and_category(
            month=month, cat=cat
        )
        if rows and cat in rows[0]:
            # budget with the given category already exists
            print("You already budgeted this category for the given month")
        else:
            await self.bud_manager.append(row)

    def execute(self) -> None:
        try:
            with task_progress(description="Processing.."):
                asyncio.run(self.add_budget())
                print(":heavy_check_mark: Budget was added successfully")
        except AttributeError:
            print("Init factory manager error")
