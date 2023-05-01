import typer
from rich import print

from .auth import get_user_authorization
from .cli import add, config, display
from .commands import InitCommand

# init typer app
app = typer.Typer()

# register commands
app.add_typer(config.app, name="config")
app.add_typer(add.app, name="add")
app.add_typer(display.app, name="list")


@app.command()
def auth():
    """Authorize the app to use the user data"""
    try:
        get_user_authorization()
        print(":heavy_check_mark: User authorized successfully")
    except Exception as e:
        print(":x: Error authorizing user")
        print(e)


@app.command()
def init():
    """Init the sheets in the Google spreadsheets"""
    command = InitCommand()
    command.execute()


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        ctx.get_help()


if __name__ == "__main__":
    app()
