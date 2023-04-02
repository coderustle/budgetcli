"""
This module contains the commands for adding transactions to the google sheet
"""
import typer
from rich import print

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
    print(date)
    print(category)
    print(description)
    print(amount)


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
