"""
This module contains different settings used accross the application
"""
import os

from platformdirs import user_config_dir

APP_NAME = "budgetcli"
CONFIG_FILE_NAME = "config.json"
USER_CONFIG_DIR = user_config_dir(APP_NAME, ensure_exists=True)
CONFIG_FILE_PATH = os.path.join(USER_CONFIG_DIR, CONFIG_FILE_NAME)
CREDENTIALS_SECRET_PATH = os.path.join(USER_CONFIG_DIR, "credentials.json")
