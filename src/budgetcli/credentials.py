"""
This module contains the implementation for get_credentials function used
to autorize the application and to initiate the user that authorization flow.
"""
import os

from rich import print
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.auth.external_account_authorized_user import (
    Credentials as ExCredentials,
)
from google_auth_oauthlib.flow import InstalledAppFlow

from .settings import AUTH_TOKEN_PATH, SCOPES, CREDENTIALS_SECRET_PATH


def get_credentials() -> Credentials | ExCredentials | None:
    """This function is used to get the user data authorization"""

    credentials: Credentials | ExCredentials | None = None

    # check if token.json exists in the app config dir
    if os.path.exists(AUTH_TOKEN_PATH):
        credentials = Credentials.from_authorized_user_file(
            AUTH_TOKEN_PATH, SCOPES
        )
        return credentials

    # if token.json is not there, let the user login
    if os.path.isfile(CREDENTIALS_SECRET_PATH):
        flow = InstalledAppFlow.from_client_secrets_file(
            CREDENTIALS_SECRET_PATH, SCOPES
        )

        credentials = flow.run_local_server(port=0)

        with open(AUTH_TOKEN_PATH, "w") as file:
            file.write(credentials.to_json())

        return credentials

    else:
        print(":x: The client_secret.json file is missing")

    return credentials
