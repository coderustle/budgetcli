"""
This module contains different settings used accross the application
"""
import os

from platformdirs import user_config_dir

APP_NAME = "budgetcli"
CURRENCY = "$"
CONFIG_FILE_NAME = "config.json"
USER_CONFIG_DIR = user_config_dir(APP_NAME, ensure_exists=True)
CONFIG_FILE_PATH = os.path.join(USER_CONFIG_DIR, CONFIG_FILE_NAME)
CREDENTIALS_SECRET_PATH = os.path.join(USER_CONFIG_DIR, "credentials.json")
AUTH_TOKEN_PATH = os.path.join(USER_CONFIG_DIR, "token.json")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
API_SERVICE_NAME = "sheets"
API_VERSION = "v4"
API_URL = "https://sheets.googleapis.com/v4/spreadsheets"
GVI_URL = "https://docs.google.com/spreadsheets/d"
