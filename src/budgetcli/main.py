import typer
from rich import print

from .auth import get_user_authorization
from .commands import add, config
from .data_manager import GoogleSheetManager

# init typer app
app = typer.Typer()

# register commands
app.add_typer(config.app, name="config")
app.add_typer(add.app, name="add")


@app.command()
def auth():
    """Authorize the app to use the user data"""
    get_user_authorization()


@app.command()
def init():
    """Init the tables in the google sheet"""
    manager = GoogleSheetManager()

    manager.init_sheets()
    print(":heavy_check_mark: Tables initialized succesfuly")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        ctx.get_help()


if __name__ == "__main__":
    app()
