from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from app.models.user import UserLogin

router = APIRouter(
    prefix="/users",
    tags=["forms"],
    dependencies=[Depends(get)]
)

@router.post('/login')
def login(user: UserLogin, Authorize: AuthJWT = Depends()):
    if user.username != "test" or user.password != "test":
        raise HTTPException(status_code=401,detail="Bad username or password")

    # subject identifier for who this token is for example id or username from database
    access_token = Authorize.create_access_token(subject=user.username)
    return {"access_token": access_token}


# protect endpoint with function jwt_required(), which requires
# a valid access token in the request headers to access.
@router.get('/user')
def user(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}
