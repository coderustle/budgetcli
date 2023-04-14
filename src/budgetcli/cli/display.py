
import typer

from ..commands import ListTransactionCommand

app = typer.Typer()

@app.command()
def transactions():
    """List all transactions from spreadsheet"""
    command = ListTransactionCommand()
    command.execute()

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """List data from google spreadsheet"""
    if ctx.invoked_subcommand is None:
        ctx.get_help()
