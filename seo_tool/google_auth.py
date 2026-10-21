"""Google-credentials voor Search Console en GA4.

Twee manieren, in deze volgorde:
1. Service account: GOOGLE_APPLICATION_CREDENTIALS wijst naar een JSON-sleutel.
   Voeg het e-mailadres van het service account toe aan elke GSC-property en GA4-property.
2. OAuth als jezelf: credentials/client_secret.json (Desktop app). Bij de eerste run
   opent een browser; het token wordt bewaard in credentials/token.json.
"""

from __future__ import annotations

import os
from pathlib import Path

from .clients import ROOT

SCOPES = [
    "https://www.googleapis.com/auth/webmasters.readonly",
    "https://www.googleapis.com/auth/analytics.readonly",
]

CRED_DIR = ROOT / "credentials"


def get_credentials():
    sa_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if sa_path:
        from google.oauth2 import service_account

        path = Path(sa_path)
        if not path.is_absolute():
            path = ROOT / path
        if not path.exists():
            raise SystemExit(f"Service-account-sleutel niet gevonden: {path}")
        return service_account.Credentials.from_service_account_file(str(path), scopes=SCOPES)

    secret = CRED_DIR / "client_secret.json"
    token = CRED_DIR / "token.json"
    if not secret.exists() and not token.exists():
        raise SystemExit(
            "Geen Google-credentials. Zet GOOGLE_APPLICATION_CREDENTIALS in .env "
            "of plaats credentials/client_secret.json. Zie docs/google-koppelen.md."
        )

    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials

    creds = Credentials.from_authorized_user_file(str(token), SCOPES) if token.exists() else None
    if creds and creds.valid:
        return creds
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        from google_auth_oauthlib.flow import InstalledAppFlow

        flow = InstalledAppFlow.from_client_secrets_file(str(secret), SCOPES)
        creds = flow.run_local_server(port=0)
    CRED_DIR.mkdir(exist_ok=True)
    token.write_text(creds.to_json())
    return creds
