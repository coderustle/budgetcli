import typer

from .commands import config

# init typer app
app = typer.Typer()

# register commands
app.add_typer(config.app, name="config")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        ctx.get_help()


if __name__ == "__main__":
    app()
