"""
This module contains the config command
"""
import json
import os

import typer
from platformdirs import user_config_dir
from rich import print

from ..settings import APP_NAME, CONFIG_FILE_NAME

app = typer.Typer()


@app.command()
def spreadsheet(spreadsheet_id: str) -> None:
    """Provide the google spreadsheet id to be used and store data"""

    config = {
        "spreadsheet_id": spreadsheet_id,
    }

    config_dir = user_config_dir(APP_NAME, ensure_exists=True)
    config_file_path = os.path.join(config_dir, CONFIG_FILE_NAME)

    with open(config_file_path, "w") as config_file:
        json.dump(config, config_file, indent=2)

    print(":heavy_check_mark: Spreadsheet id was updated")


@app.command()
def secret(path: str) -> None:
    """Provide the client_secret.json path to be copied in config folder"""
    print(path)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        ctx.get_help()


if __name__ == "__main__":
    app()
