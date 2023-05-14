"""
This module contains the commands for adding transactions to the Google sheet
"""
from datetime import date as date_obj
from decimal import Decimal

import typer

from ..commands import (
    AddTransactionCommand,
    AddCategoryCommand,
    AddBudgetCommand,
)
from ..models import (
    Transaction,
    Category,
    validate_amount,
    validate_date,
    Budget,
)
from ..utils.dates import get_today_date

app = typer.Typer()

DateArgument = typer.Option(get_today_date())
CategoryArgument = typer.Argument(...)
DescriptionArgument = typer.Option("")
AmountArgument = typer.Argument(...)


@app.command(name="category")
def category_entry(name: str = CategoryArgument):
    """Add budget/transaction category"""
    if name:
        cat = Category(name)
        command = AddCategoryCommand(cat)
        command.execute()


@app.command(name="budget")
def budget_entry(
    category: str = CategoryArgument,
    amount: str = AmountArgument,
    date: str = DateArgument,
):
    """Add budget for category"""
    budget_entry_date: date_obj | None = validate_date(date)
    budget_entry_amount: Decimal | None = validate_amount(amount)
    if budget_entry_date and budget_entry_amount:
        budget = Budget(date=budget_entry_date, category=category)
        budget.amount = budget_entry_amount
        command = AddBudgetCommand(budget)
        command.execute()


@app.command(name="income")
def income_entry(
    amount: str = AmountArgument,
    category: str = CategoryArgument,
    description: str = DescriptionArgument,
    date: str = DateArgument,
):
    """Add an income transaction"""
    parsed_date: date_obj | None = validate_date(date)
    parsed_amount: Decimal | None = validate_amount(amount)

    if parsed_date and parsed_amount:
        transaction = Transaction(parsed_date, category, description)
        transaction.income = parsed_amount
        command = AddTransactionCommand(transaction)
        command.execute()


@app.command(name="outcome")
def outcome_entry(
    amount: str = AmountArgument,
    category: str = CategoryArgument,
    description: str = DescriptionArgument,
    date: str = DateArgument,
):
    """Add an outcome transaction"""
    parsed_date: date_obj | None = validate_date(date)
    parsed_amount: Decimal | None = validate_amount(amount)

    if parsed_date and parsed_amount:
        transaction = Transaction(parsed_date, category, description)
        transaction.outcome = parsed_amount
        command = AddTransactionCommand(transaction)
        command.execute()


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Add data to the Google sheet"""
    if not ctx.invoked_subcommand:
        ctx.get_help()


if __name__ == "__main__":
    app()
