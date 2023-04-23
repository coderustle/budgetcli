import typer

from ..commands import ListTransactionCommand

app = typer.Typer()

RowsOption = typer.Option(100, min=1, max=100, help="Number of rows")
MonthOption = typer.Option(None)


@app.command()
def transactions(rows: int = RowsOption):
    """List all transactions from spreadsheet"""
    command = ListTransactionCommand(rows)
    command.execute()


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """List data from google spreadsheet"""
    if ctx.invoked_subcommand is None:
        ctx.get_help()
