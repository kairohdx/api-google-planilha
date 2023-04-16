
from fastapi import HTTPException
from app.settings import Settings
from app.sheetAPI.sheetCreds import SheetCred

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class ConsumeAPI:
    def __init__(self) -> None:
        settings:Settings = Settings()
        self.spreadsheetId = settings.sheet_id
        self.sheetCreds = SheetCred(settings.sheet_scopes)
        self.creds = self.sheetCreds.creds

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

