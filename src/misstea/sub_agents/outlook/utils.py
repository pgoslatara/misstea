import json
import logging
import os
from pathlib import Path
from zoneinfo import ZoneInfo

import requests
from O365 import Account
from O365.utils import FileSystemTokenBackend

from misstea.constants import OUTLOOK_TOKEN_PATH

logger = logging.getLogger(__name__)


def generate_outlook_token() -> None:
    """Use the Microsoft 365 API to generate a new access token to access their API. This token is valid for 90 days and should be stored in file named o365_token.txt in the root directory of this repository.

    Raises:
        RuntimeError: If MICROSOFT_CLIENT_ID, MICROSOFT_CLIENT_SECRET, or TENANT_ID environment variables are not set.

    """
    Path(OUTLOOK_TOKEN_PATH / "o365_token.txt").unlink(missing_ok=True)

    logger.info("Requesting access token...")
    client_id = os.getenv("MICROSOFT_CLIENT_ID")
    client_secret = os.getenv("MICROSOFT_CLIENT_SECRET")
    tenant_id = os.getenv("TENANT_ID")

    if not client_id or not client_secret or not tenant_id:
        raise RuntimeError(
            "MICROSOFT_CLIENT_ID, MICROSOFT_CLIENT_SECRET, and TENANT_ID environment variables must be set."
        )

    r_access_token = requests.post(
        f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token",
        data={
            "client_id": client_id,
            "scope": "https://graph.microsoft.com/.default",
            "client_secret": client_secret,
            "grant_type": "client_credentials",
        },
        timeout=10,  # Added timeout to requests call
    )

    logger.info("Saving access token to file...")
    logger.debug(f"{OUTLOOK_TOKEN_PATH=}")
    with Path.open(OUTLOOK_TOKEN_PATH / "o365_token.txt", "w") as f:
        json.dump(r_access_token.json(), f)

    logger.info("Requesting refresh token, manual input/verification required...")
    credentials = (client_id, client_secret)
    scopes = ["basic", "calendar_all", "message_all"]
    account = Account(
        credentials=credentials,
        token_backend=FileSystemTokenBackend(
            token_filename="o365_token.txt",  # noqa: S106
            token_path=OUTLOOK_TOKEN_PATH,
        ),
        timezone=ZoneInfo("Europe/Amsterdam"),
    )
    account.authenticate(requested_scopes=scopes)
    logger.info("Authenticated to Office365.")
