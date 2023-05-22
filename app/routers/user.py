from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi_jwt_auth import AuthJWT
from app.data.user import DataUser
from app.auth import pwd_context
from app.dependencies import protected
from app.models.auth import AuthBase, AuthResponse
from app.models.user import UserBase, UserLogin, UserPost


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post('/login', response_model=AuthResponse)
async def login(user_post: AuthBase, current_user: UserBase = Depends(protected), Authorize: AuthJWT = Depends()):
    dbObj = DataUser()
    if (user := await dbObj.getByEmail(user_post.email)) is not None:
        if not pwd_context.verify(user_post.password, user.passHash):
            raise HTTPException(status_code=401,detail="E-mail ou senha invalido!")
    
    auth = AuthResponse()
    auth.access_token = Authorize.create_access_token(subject=user_post.email, expires_time=auth.expire_in)
    auth.refresh_token = Authorize.create_refresh_token(subject=user_post.email)
    
    return auth


@router.get('/{_id}', response_model=UserBase)
async def getUserById(_id:str, current_user: UserBase = Depends(protected)):
    if current_user.scope == "admin":
        dataUser:DataUser = DataUser()
        if (user := await dataUser.getById(_id)):
            return user
        raise HTTPException(status_code=404, detail="Usuario não encontrado")
    raise HTTPException(status_code=403, detail="Este usuario não tem permição para ciar novos usuarios!")


@router.post('/', response_model=UserBase)
async def newUser(user:UserPost, current_user: UserBase = Depends(protected)):
    print(current_user.dict())
    if current_user.scope == "public":
        dataUser:DataUser = DataUser()

        user.passHash = pwd_context.hash(user.passHash)
        return await dataUser.insertUser(user)
    raise HTTPException(status_code=403, detail="Este usuario não tem permição para ciar novos usuarios!")
