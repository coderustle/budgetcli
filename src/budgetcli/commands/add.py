"""
This module contains the commands for adding transactions to the google sheet
"""
import typer
from rich import print

from ..transactions import RecordType

app = typer.Typer()


@app.command()
def transaction(type: RecordType):
    """Add a transaction to the google sheet"""
    print(type)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Add transactions to the google sheet"""
    if not ctx.invoked_subcommand:
        ctx.get_help()


if __name__ == "__main__":
    app()
