from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi_jwt_auth import AuthJWT
from app.data.user import DataUser

from app.models.auth import AuthBase, AuthResponse
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/", response_model=AuthResponse)
async def auth(authBody:AuthBase, Authorize: AuthJWT = Depends()):
    dbObj = DataUser()
    if (user := await dbObj.getByEmail(authBody.email)) is not None:
        if not pwd_context.verify(authBody.password, user.passHash):
            raise HTTPException(status_code=401,detail="E-mail ou senha invalido!")
    
    auth = AuthResponse()
    auth.access_token = Authorize.create_access_token(subject=authBody.email, expires_time=auth.expire_in)
    auth.refresh_token = Authorize.create_refresh_token(subject=authBody.email)
    
    return auth

@router.post('/refresh', include_in_schema=False)
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}