"""
This module contains the commands for adding transactions to the google sheet
"""
import typer

app = typer.Typer()


@app.callback()
def main(ctx: typer.Context):
    """Add transactions to the google sheet"""
    if not ctx.invoked_subcommand:
        ctx.get_help()


if __name__ == "__main__":
    app()
