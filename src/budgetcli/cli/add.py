"""
This module contains the commands for adding transactions to the Google sheet
"""
from datetime import date as date_obj
from decimal import Decimal

import typer

from ..commands import AddTransactionCommand, AddCategoryCommand
from ..models import Transaction, Category, validate_amount, validate_date
from ..utils.dates import get_today_date

app = typer.Typer()

DateArgument = typer.Option(
    get_today_date(), help="The date of the transaction"
)
CategoryArgument = typer.Argument(..., help="The category of the transaction")
DescriptionArgument = typer.Option("", help="Transaction description")
AmountArgument = typer.Argument(..., help="The amount of the transaction")


@app.command()
def category(name: str = CategoryArgument):
    """Add a category to Google sheet"""
    if name:
        cat = Category(name)
        command = AddCategoryCommand(cat)
        command.execute()


@app.command()
def income(
    amount: str = AmountArgument,
    category: str = CategoryArgument,
    description: str = DescriptionArgument,
    date: str = DateArgument,
):
    """Add an income transaction to the Google sheet"""
    parsed_date: date_obj | None = validate_date(date)
    parsed_amount: Decimal | None = validate_amount(amount)

    if parsed_date and parsed_amount:
        transaction = Transaction(parsed_date, category, description)
        transaction.income = parsed_amount
        command = AddTransactionCommand(transaction)
        command.execute()


@app.command()
def outcome(
    amount: str = AmountArgument,
    category: str = CategoryArgument,
    description: str = DescriptionArgument,
    date: str = DateArgument,
):
    """Add an outcome transaction to the Google sheet"""
    parsed_date: date_obj | None = validate_date(date)
    parsed_amount: Decimal | None = validate_amount(amount)

    if parsed_date and parsed_amount:
        transaction = Transaction(parsed_date, category, description)
        transaction.outcome = parsed_amount
        command = AddTransactionCommand(transaction)
        command.execute()


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Add transactions to the Google sheet"""
    if not ctx.invoked_subcommand:
        ctx.get_help()


if __name__ == "__main__":
    app()
