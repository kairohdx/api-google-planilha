from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi_jwt_auth import AuthJWT
from app.data.user import DataUser
from app.auth import pwd_context
from app.dependencies import protected
from app.models.auth import AuthResponse
from app.models.user import UserBase, UserLogin, UserPost


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post('/login', response_model=AuthResponse)
def login(user: UserLogin, current_user: UserBase = Depends(protected), Authorize: AuthJWT = Depends()):
    if user.email != "test2" or user.password != "test2":
        raise HTTPException(status_code=401, detail="E-mail ou senha invalidos!")
    
    auth = AuthResponse()
    auth.access_token = Authorize.create_access_token(subject=user.email, expires_time=auth.expire_in)
    auth.refresh_token = Authorize.create_refresh_token(subject=user.email)
    
    return auth


@router.get('/{_id}', response_model=UserBase)
def getUserById(current_user: UserBase = Depends(protected)):
    return current_user


@router.post('/', response_model=UserBase)
async def newUser(user:UserPost, current_user: UserBase = Depends(protected)):
    if current_user.email == "kairohdx.faria@gmail.com":
        dataUser:DataUser = DataUser()

        user.passHash = pwd_context.hash(user.passHash)
        return await dataUser.insertUser(user)
    raise HTTPException(status_code=403 ,detail="Este usuario não tem permição para ciar novos usuarios!")
