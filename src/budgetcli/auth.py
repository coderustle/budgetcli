"""
This module contains the implementation for get_credentials function used
to autorize the application and to initiate the user that authorization flow.
"""
import os

from google.auth.external_account_authorized_user import (
    Credentials as ExCredentials,
)
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from rich import print

from .settings import AUTH_TOKEN_PATH, CREDENTIALS_SECRET_PATH, SCOPES


def get_user_authorization() -> ExCredentials | Credentials | None:
    """This function is used to get the user data authorization"""

    credentials: Credentials | ExCredentials | None = None

    # if token.json is not there, let the user login
    if os.path.isfile(CREDENTIALS_SECRET_PATH):
        flow = InstalledAppFlow.from_client_secrets_file(
            CREDENTIALS_SECRET_PATH, SCOPES
        )

        credentials = flow.run_local_server(port=60880)

        with open(AUTH_TOKEN_PATH, "w") as file:
            file.write(credentials.to_json())

    else:
        print(":x: The client_secret.json file is missing")

    return credentials


def load_user_token() -> Credentials | None:
    """This function is used to get the user data authorization"""

    credentials: Credentials | None = None

    # check if token.json exists in the app config dir
    if os.path.exists(AUTH_TOKEN_PATH):
        credentials = Credentials.from_authorized_user_file(
            AUTH_TOKEN_PATH, SCOPES
        )

        if not credentials or not credentials.valid:
            if (
                credentials
                and credentials.expired
                and credentials.refresh_token
            ):
                credentials.refresh(Request())
            else:
                return None

        return credentials

    return None
