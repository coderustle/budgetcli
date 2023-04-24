import calendar
import typer

from ..commands import ListTransactionCommand
from ..utils import dates

app = typer.Typer()


def validate_month(value: str | None) -> str | None:
    """A callback function to validate month input"""
    if value:
        value_str = value.lower()
        for i, month in enumerate(calendar.month_name[1:], 1):
            abbr = calendar.month_abbr[i].lower()
            if value_str != month.lower() or value_str != abbr:
                error = "Invalid month name. Ex: March or Mar"
                raise typer.BadParameter(error)
            else:
                return value
    return value


RowsOption = typer.Option(100, min=1, max=100, help="Number of rows")
MonthOption = typer.Option(
    "", help="The name of the month", callback=validate_month
)


@app.command()
def transactions(rows: int = RowsOption, month: str = MonthOption):
    """List all transactions from spreadsheet"""
    month_number = dates.get_month_number(month)
    command = ListTransactionCommand(rows, month_number)
    command.execute()


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """List data from google spreadsheet"""
    if ctx.invoked_subcommand is None:
        ctx.get_help()
