import calendar
import typer

from ..utils.config import get_config_list
from ..commands import ListTransactionCommand, ListCategoryCommand
from ..utils import dates

app = typer.Typer()


def validate_month(value: str | None) -> str | None:
    """A callback function to validate month input"""
    if value:
        value = value.lower()
        month_names = [month.lower() for month in calendar.month_name[1:]]
        month_abbr = [abbr.lower() for abbr in calendar.month_abbr[1:]]
        if value in month_names or value in month_abbr:
            return value
        else:
            error = f"Invalid month name {value}. Ex: March or Mar"
            raise typer.BadParameter(error)
    return value


RowsOption = typer.Option(
    100,
    min=1,
    max=100,
    help="Number of transaction rows to display",
)
NameOption = typer.Option("", help="The name of category")
MonthOption = typer.Option(
    "",
    help="The name of the month eg: April or Apr",
    callback=validate_month,
)


@app.command()
def categories(rows: int = RowsOption, name: str = NameOption):
    """List all categories from spreadsheet"""
    command = ListCategoryCommand(rows=rows, name=name)
    command.execute()


@app.command()
def transactions(rows: int = RowsOption, month: str = MonthOption):
    """List all transactions from spreadsheet"""
    month_number = dates.get_month_number(month)
    command = ListTransactionCommand(rows, month_number)
    command.execute()


@app.command()
def config():
    """List all the settings from config.json"""

    get_config_list()


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """List data from google spreadsheet"""
    if ctx.invoked_subcommand is None:
        ctx.get_help()
