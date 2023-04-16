
import os.path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow



class SheetCred:

    def __init__(self, scope) -> None:
        self.scope = scope
        creds = None
        if not os.path.exists('token.json'):
            self.creds = creds
            return 
        creds = Credentials.from_authorized_user_file('token.json', self.scope)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
        self.creds = creds

    async def genTokenFile(self):
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', self.scope)
        creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())