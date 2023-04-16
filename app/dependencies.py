from typing import Annotated
from fastapi import Depends, HTTPException, Header
from app.models.user import UserBase
from app.settings import Settings
from fastapi_jwt_auth import AuthJWT

#load config
def get_settings():
    return Settings()

async def current_user(email:str | None = None):
    if email:
        if email == "usuario.publico@email.com":#'kairohdx.faria@gmail.com'
            return UserBase(name="Folha", email="kairohdx.faria@gmail.com", scope="Admin")
    return None


async def pagination(q: str = "", page: int = 1, limit: int = 10):
    return {"q": q, "page": page, "limit": limit}

async def db_obj(config: Annotated[Settings, Depends(get_settings)]):
    return config.db



async def protected(authorization: Annotated[str, Header()] = "Bearer ", Authorize: AuthJWT = Depends()) -> UserBase:
    Authorize.jwt_required()
    if (user := await current_user(Authorize.get_jwt_subject())) is not None:
        return user
    raise HTTPException(status_code=403,detail="Requisição não permitida para o scopo do usuario")
