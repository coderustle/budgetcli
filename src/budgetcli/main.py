import typer
from rich import print

from .auth import get_user_authorization
from .cli import add, config
from .data_manager import get_data_manager

# init typer app
app = typer.Typer()

# register commands
app.add_typer(config.app, name="config")
app.add_typer(add.app, name="add")


@app.command()
def auth():
    """Authorize the app to use the user data"""
    try:
        get_user_authorization()
        print(":heavy_check_mark: User authorized succesfuly")
    except Exception as e:
        print(":x: Error authorizing user")
        print(e)


@app.command()
def init():
    """Init the tables in the google sheet"""
    manager = get_data_manager()

    if manager:
        try:
            manager.init_sheets_headers()
            print(":heavy_check_mark: Table headers initialized succesfuly")
        except Exception as e:
            print(":x: Error initializing tables")
            print(e)
    else:
        print(":x: Error initializing tables")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        ctx.get_help()


if __name__ == "__main__":
    app()
