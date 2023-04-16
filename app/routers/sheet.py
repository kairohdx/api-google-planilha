from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from app.models.pageSheet import PageSheet
from app.settings import Settings

from app.sheetAPI.consume import ConsumeAPI
from app.sheetAPI.sheetCreds import SheetCred

router = APIRouter(
    prefix="/sheets",
    tags=["sheets"]
)

@router.get('/')
async def genToken():
    consumeAPI = ConsumeAPI()
    if not consumeAPI.creds:
        await consumeAPI.sheetCreds.genTokenFile()
        return {"Mensagem": "Arquivo criado!"}
    return {"Mensagem":"Arquivo já existente!"}

@router.post('/', response_model=dict)
async def append_row_in_sheet(pageSheet:PageSheet, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    consumeAPI = ConsumeAPI()
    if consumeAPI.creds:
        return {"FileAndPageStatus": await consumeAPI.apend_row(pageSheet.pageName, pageSheet.values)}
    raise HTTPException(status_code=404, detail="Arquivo Token.json não encontrado!")

@router.post('/new_page', response_model=dict)
async def new_page(pageSheet:PageSheet, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    consumeAPI = ConsumeAPI()
    if consumeAPI.creds:
        return {"FileAndPageStatus": await consumeAPI.new_page(pageSheet.pageName, pageSheet.firstLine)}
    raise HTTPException(status_code=404, detail="Arquivo Token.json não encontrado!")
