"""
This module contains the config command
"""
import os
import shutil

import typer
from rich import print

from ..settings import (
    CREDENTIALS_SECRET_PATH,
    USER_CONFIG_DIR,
)
from ..utils import get_config_list, update_config

app = typer.Typer()


@app.command(name="list")
def list_config():
    """List all the settings from config.json"""

    get_config_list()


@app.command()
def spreadsheet(spreadsheet_id: str) -> None:
    """Provide the google spreadsheet id to be used and store data"""

    update_config("spreadsheet_id", spreadsheet_id)


@app.command()
def credentials(path: str) -> None:
    """
    Provide the absolute path to client_secret.json file
    to be copied in app config folder
    """

    # check if the provided path exists
    if os.path.isfile(path):
        shutil.copy(path, CREDENTIALS_SECRET_PATH)
        update_config("client_secret", CREDENTIALS_SECRET_PATH)

        print(f":heavy_check_mark: File copied succesfuly to {USER_CONFIG_DIR}")
    else:
        print(f':x: The provided file path to "{path}" is not correct')


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """Manage the configuration of the app"""
    if ctx.invoked_subcommand is None:
        ctx.get_help()


if __name__ == "__main__":
    app()
