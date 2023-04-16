from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from app.data.form import DataForm

from app.dependencies import db_obj, pagination, protected
from app.models.form import FormComplete, FormLayoutBase
from app.models.user import UserBase

router = APIRouter(
    prefix="/forms",
    tags=["forms"]
)

@router.get("/", response_model=list[FormLayoutBase])
async def read_forms(searh: dict = Depends(pagination), Authorize: AuthJWT = Depends(), db: Any = Depends(db_obj)):
    Authorize.jwt_required()
    return [{"form1":"sucesso"}]

@router.get("/{idform}", response_model=FormComplete)
async def read_form(idForm: str, Authorize: AuthJWT = Depends(), db: Any = Depends(db_obj)):
    return {"_id": idForm}

@router.post('/', response_model=FormComplete)
async def newForm(user:FormComplete, current_user: UserBase = Depends(protected)):
    scopes = ["admin", "sistem_adm"]
    if current_user.scope.lower() in scopes:
        dataForm:DataForm = DataForm()
        return await dataForm.insertForm(user)
    raise HTTPException(status_code=403 ,detail="Este usuario não tem permição para ciar novos Formularios!")
