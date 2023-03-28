import typer

from .commands import config
from .commands import auth

# init typer app
app = typer.Typer()

# register commands
app.add_typer(config.app, name="config")
app.add_typer(auth.app, name="auth")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        ctx.get_help()


if __name__ == "__main__":
    app()
