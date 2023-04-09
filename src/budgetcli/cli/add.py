"""
This module contains the commands for adding transactions to the google sheet
"""

import typer

from ..models import Transaction, validate_date, validate_amount
from ..commands import AddTransactionCommand

app = typer.Typer()

DateArgument = typer.Argument(..., help="The date of the transaction")
CategoryArgument = typer.Argument(..., help="The category of the transaction")
DescriptionArgument = typer.Argument(..., help="Transaction description")
AmountArgument = typer.Argument(..., help="The amount of the transaction")


@app.command()
def income(
    date: str = DateArgument,
    category: str = CategoryArgument,
    description: str = DescriptionArgument,
    amount: str = AmountArgument,
):
    """Add an income transaction to the google sheet"""
    transaction: Transaction | None = None

    parsed_date = validate_date(date)
    parsed_amount = validate_amount(amount)

    if parsed_date and parsed_amount:
        transaction = Transaction(parsed_date, category, description)
        transaction.income = parsed_amount

    if transaction:
        command = AddTransactionCommand(transaction)
        command.execute()


@app.command()
def outcome(
    date: str = DateArgument,
    category: str = CategoryArgument,
    description: str = DescriptionArgument,
    amount: str = AmountArgument,
):
    """Add an outcome transaction to the google sheet"""
    transaction: Transaction | None = None

    parsed_date = validate_date(date)
    parsed_amount = validate_amount(amount)

    if parsed_date and parsed_amount:
        transaction = Transaction(parsed_date, category, description)
        transaction.outcome = parsed_amount

    if transaction is not None:
        command = AddTransactionCommand(transaction)
        command.execute()


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Add transactions to the google sheet"""
    if not ctx.invoked_subcommand:
        ctx.get_help()


if __name__ == "__main__":
    app()
