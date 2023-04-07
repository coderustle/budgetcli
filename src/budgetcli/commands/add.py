"""
This module contains the commands for adding transactions to the google sheet
"""

import typer
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn

from ..transactions import Transaction, validate_date, validate_amount
from ..data_manager import get_data_manager, GoogleSheetManager

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
    manager: GoogleSheetManager | None = get_data_manager()

    parsed_date = validate_date(date)
    parsed_amount = validate_amount(amount)

    if parsed_date and parsed_amount:
        transaction = Transaction(parsed_date, category, description)
        transaction.income = parsed_amount

    if manager and transaction:
        column1 = SpinnerColumn()
        column2 = TextColumn("Processing..")

        with Progress(column1, column2, transient=True) as progress:
            progress.add_task("Add transaction", total=None)
            result = manager.add_transaction(transaction.to_sheet_row())
            if result:
                print(":heavy_check_mark: Transaction was added successfully")


@app.command()
def outcome(
    date: str = DateArgument,
    category: str = CategoryArgument,
    description: str = DescriptionArgument,
    amount: str = AmountArgument,
):
    """Add an outcome transaction to the google sheet"""
    print(date)
    print(category)
    print(description)
    print(amount)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Add transactions to the google sheet"""
    if not ctx.invoked_subcommand:
        ctx.get_help()


if __name__ == "__main__":
    app()
