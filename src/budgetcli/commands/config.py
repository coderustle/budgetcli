"""
This module contains the config command
"""
import json
import os
import shutil

import typer
from rich import print

from ..settings import (
    CONFIG_FILE_PATH,
    CREDENTIALS_SECRET_PATH,
    USER_CONFIG_DIR,
)

app = typer.Typer()


@app.command()
def spreadsheet(spreadsheet_id: str) -> None:
    """Provide the google spreadsheet id to be used and store data"""

    if os.path.exists(CONFIG_FILE_PATH):
        config: dict

        # load the current file if exists and update spreadsheet id
        with open(CONFIG_FILE_PATH) as file:
            config = json.load(file)
            config["spreadsheet_id"] = spreadsheet_id

        # write the updated data to config.json
        with open(CONFIG_FILE_PATH, "w") as file:
            json.dump(config, file, indent=2)
        print(":heavy_check_mark: Spreadsheet id was updated")

    else:
        # create and write the data to config.json
        config = {"spreadsheet_id": spreadsheet_id}

        with open(CONFIG_FILE_PATH, "w") as file:
            json.dump(config, file, indent=2)

        print(":heavy_check_mark: Spreadsheet id was created")


@app.command()
def secret(path: str) -> None:
    """
    Provide the absolute client_secret.json
    path to be copied in config folder
    """

    # check if the provided path exists
    if os.path.isfile(path):
        shutil.copy(path, CREDENTIALS_SECRET_PATH)
        print(f":heavy_check_mark: File copied succesfuly to {USER_CONFIG_DIR}")
    else:
        print(f':x: The provided file path to "{path}" is not correct')


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        ctx.get_help()


if __name__ == "__main__":
    app()
