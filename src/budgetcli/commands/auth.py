"""
This module contains the command to authorize the user data in google.
"""

import typer

from ..credentials import get_user_authorization


app = typer.Typer()


@app.callback(invoke_without_command=True)
def main() -> None:
    """Authorize the app to use the user data"""
    get_user_authorization()


if __name__ == "__main__":
    app()
