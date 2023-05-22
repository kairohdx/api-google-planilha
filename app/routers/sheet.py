from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from app.data.form import DataForm
from app.data.user import DataUser
from app.models.form import FormComplete
from app.models.pageSheet import PageSheet
from app.models.user import UserBase
from google.oauth2.credentials import Credentials

from app.sheetAPI.consume import ConsumeAPI

router = APIRouter(
    prefix="/sheets",
    tags=["sheets"]
)

    

@router.post('/', response_model=dict)
async def append_row_in_sheet(sheetsId:str, userId:str, pageSheet:PageSheet, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    dbObj:DataForm = DataForm()
    form:FormComplete = await dbObj.getBySheetAndUser(sheetsId, userId)

    if form:
        consumeAPI = ConsumeAPI()
        consumeAPI.setSheetsId(sheetsId)
        if consumeAPI.creds:
            return {"FileAndPageStatus": await consumeAPI.apend_row(pageSheet.pageName, pageSheet.values)}
        raise HTTPException(status_code=404, detail="Credenciais de Token não configuradas!")
    raise HTTPException(status_code=404, detail="Formulario não encontrado!")


@router.post('/new_page', response_model=dict)
async def new_page(formId:str, pageSheet:PageSheet, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    dbObj:DataForm = DataForm()
    form:FormComplete = await dbObj.getById(formId)

    consumeAPI = ConsumeAPI()
    consumeAPI.setSheetsId(form.sheetsId)
    if consumeAPI.creds:
        return {"FileAndPageStatus": await consumeAPI.new_page(pageSheet.pageName, pageSheet.firstLine)}
    raise HTTPException(status_code=404, detail="Arquivo Token.json não encontrado!")
