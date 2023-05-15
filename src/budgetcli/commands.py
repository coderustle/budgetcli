import asyncio
from abc import ABC, abstractmethod

from rich import print

from .data_manager import (
    ManagerFactory,
    Client,
    TransactionDataManager,
    CategoryDataManager,
    BudgetDataManager,
)
from .models import Transaction, Category, Budget
from .settings import CURRENCY
from .utils.display import (
    get_transaction_table,
    task_progress,
    get_category_table,
)


class Command(ABC):
    @abstractmethod
    async def execute(self) -> None:
        raise NotImplementedError


class InitCommand(Command):
    async def execute(self) -> None:
        async with Client() as session:
            tra_manager = TransactionDataManager(session)
            cat_manager = CategoryDataManager(session)
            bud_manager = BudgetDataManager(session)
            tasks = [
                tra_manager.init(),
                cat_manager.init(),
                bud_manager.init(),
            ]
            with task_progress(description="Processing.."):
                await asyncio.gather(*tasks)
                print(":heavy_check_mark: Init was completed successfully")


class AddTransactionCommand(Command):
    def __init__(self, transaction: Transaction):
        self.transaction = transaction

    async def execute(self):
        tra_row = self.transaction.to_sheet_row()
        category_name = self.transaction.category
        async with Client() as session:
            cat_manager = CategoryDataManager(session)
            tra_manager = TransactionDataManager(session)
            categories = await cat_manager.get_records_by_name(category_name)
            with task_progress(description="Processing.."):
                if categories and category_name in categories[0]:
                    await tra_manager.append(tra_row)
                else:
                    category = Category(name=category_name)
                    row = category.to_sheet_row()
                    tasks = [
                        cat_manager.append(row),
                        tra_manager.append(tra_row),
                    ]
                    await asyncio.gather(*tasks)
                print(":heavy_check_mark: Transaction was added successfully")


class AddCategoryCommand(Command):
    def __init__(self, category: Category):
        self.category = category

    async def execute(self) -> None:
        name = self.category.name
        row = self.category.to_sheet_row()
        async with Client() as session:
            manager = CategoryDataManager(session)
            with task_progress(description="Processing.."):
                category = await manager.get_records_by_name(name)
                if not category:
                    await manager.append(row)
            print(":heavy_check_mark: Category was added successfully")


class AddBudgetCommand(Command):
    def __init__(self, budget: Budget):
        self.budget = budget

    async def execute(self):
        row = self.budget.to_sheet_row()
        cat = self.budget.category
        month = self.budget.date.month
        async with Client() as session:
            manager = BudgetDataManager(session)
            with task_progress(description="Processing.."):
                rows = await manager.get_records_by_month_and_category(
                    month=month, cat=cat
                )
                if rows and cat in rows[0]:
                    # budget with the given category already exists
                    print("You already budgeted this category")
                else:
                    await manager.append(row)


class ListTransactionCommand(Command):
    """Command to list transactions"""

    def __init__(self, rows: int, month: int | None):
        self.rows = rows
        self.month = month

    async def execute(self):
        table = get_transaction_table()
        async with Client() as session:
            manager = TransactionDataManager(session)
            with task_progress(description="Processing.."):
                if self.month:
                    get = manager.get_records_for_month(self.month)
                    transactions = asyncio.run(get)
                else:
                    get = manager.get_records(self.rows)
                    transactions = asyncio.run(get)
                for row in transactions:
                    income = f"{CURRENCY} {row[3]}"
                    outcome = f"{CURRENCY} {row[4]}"
                    table.add_row(row[0], row[1], row[2], income, outcome)
        print(table)


class ListCategoryCommand(Command):
    def __init__(self, rows: int, name: str):
        self.rows = rows
        self.name = name
        self.manager = ManagerFactory.create_manager_for("categories")

    async def execute(self) -> None:
        table = get_category_table()
        async with Client() as session:
            manager = CategoryDataManager(session)
            with task_progress(description="Processing"):
                if self.name:
                    categories = await manager.get_records_by_name(
                        name=self.name
                    )
                else:
                    categories = await manager.get_records(rows=self.rows)
                for row in categories:
                    table.add_row(row[0])
        print(table)
