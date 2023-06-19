import os
from dotenv import load_dotenv
import google_auth_oauthlib.flow
from oauth2client.client import OAuth2Credentials

scopes = ["https://www.googleapis.com/auth/spreadsheets"]


def get_token():
    load_dotenv()
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    client_secrets_file = os.path.join(os.path.abspath('../../'), os.environ.get('SECRETS_FILE'))

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        client_secrets_file, scopes)
    flow.redirect_uri = 'http://localhost:8000'

    authorization_url, _ = flow.authorization_url(prompt='consent')

    print("Click: ", authorization_url)

    code = input("Code:").strip()

    creds = flow.fetch_token(code=code)

    print(creds)

    credentials = OAuth2Credentials(
        access_token=flow.credentials.token,
        client_id=flow.credentials.client_id,
        client_secret=flow.credentials.client_secret,
        refresh_token=flow.credentials.refresh_token,
        token_expiry=flow.credentials.expiry,
        token_uri=flow.credentials.token_uri,
        user_agent=str(os.environ.get('GOOGLE_USER_AGENT')),
        id_token=flow.credentials.id_token,
        scopes=flow.credentials.scopes,
    )

    return credentials


get_token()