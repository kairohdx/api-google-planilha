
import os
from fastapi import HTTPException
from app.models.user import UserBase

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

from app.settings import Settings


class ConsumeAPI:
    def __init__(self) -> None:
        settings = Settings()
        self.spreadsheetId = ''
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        secret_file = os.path.join(os.getcwd(), settings.client_file)

        self.creds = service_account.Credentials.from_service_account_file(secret_file, scopes=scopes)

    def setSheetsId(self, spreadsheetId:str):
        self.spreadsheetId = spreadsheetId

    async def apend_row(self, pageName:str, values:list[str] = []) -> bool:

        body:dict = {
            "majorDimension": "ROWS",
            "range": f"{pageName}!A1:A",
            "values": [[value if value else '' for value in values]]
        }

        try:
            service = build('sheets', 'v4', credentials=self.creds)

            # Call the Sheets API
            request = service.spreadsheets().values().append(spreadsheetId=self.spreadsheetId, 
                                                             range=f"{pageName}!A1:A", valueInputOption="RAW", insertDataOption="INSERT_ROWS", body=body)
            request.execute()

            return True

        except HttpError as err:
            print(err)
            if err.status_code == 400:
                return False
            raise HTTPException(status_code=err.status_code, detail=err.content)

    async def new_page(self, pageName:str, values:list[str] = []) -> bool:
        service = build('sheets', 'v4', credentials=self.creds)

        body= {
            "requests":[{
                "addSheet":{
                    "properties": {
                        "title": pageName
                    }
                }
            }]
        }
        try:
            request = service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheetId, body=body)
            request.execute()

            return await self.apend_row(pageName, [str(v).title() for v in values])
        except HttpError as err:
            if err.status_code == 400:
                return False
            raise HTTPException(status_code=err.status_code, detail=err)

