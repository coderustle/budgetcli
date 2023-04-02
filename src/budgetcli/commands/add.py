"""
This module contains the commands for adding transactions to the google sheet
"""
import typer
from rich import print

from ..transactions import TransactionType

app = typer.Typer()


@app.command()
def transaction(
    date: str = typer.Argument(..., help="The date of the transaction"),
    category: str = typer.Argument(..., help="The category of the transaction"),
    description: str = typer.Argument(
        ..., help="The description of the transaction"
    ),
    amount: float = typer.Argument(..., help="The amount of the transaction"),
    type: TransactionType = typer.Option(
        ..., help="The type of the transaction"
    ),
):
    """Add a transaction to the google sheet"""
    print(type)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Add transactions to the google sheet"""
    if not ctx.invoked_subcommand:
        ctx.get_help()


if __name__ == "__main__":
    app()
