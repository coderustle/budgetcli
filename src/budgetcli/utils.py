import json
import os

from rich import print
from rich.pretty import pprint

from .settings import CONFIG_FILE_PATH


def get_config_list():
    """Utility function to list all the settings from config.json"""

    if os.path.exists(CONFIG_FILE_PATH):
        config: dict

        with open(CONFIG_FILE_PATH) as file:
            config = json.load(file)

        pprint(config, expand_all=True)

    else:
        print(":x: No config.json was found")


def update_config(setting: str, value: str) -> None:
    """Utility function to update config.json file"""

    # check if the config.json exists in app config folder
    if os.path.exists(CONFIG_FILE_PATH):
        config: dict

        # load the current configuration from config.json
        with open(CONFIG_FILE_PATH) as file:
            config = json.load(file)
            config[setting] = value

        # write the updated config back to config.json
        with open(CONFIG_FILE_PATH, "w") as file:
            json.dump(config, file, indent=2)

    else:
        # create the config.json file with the new setting
        config = {setting: value}

        with open(CONFIG_FILE_PATH, "w") as file:
            json.dump(config, file, indent=2)

    print(f":heavy_check_mark: {setting} was updated")


def get_config(setting: str) -> str | None:
    """Utility function to retrieve a setting from config.json"""

    if os.path.exists(CONFIG_FILE_PATH):
        config: dict

        with open(CONFIG_FILE_PATH) as file:
            config = json.load(file)

        return config.get(setting)
