import time
from fastapi import Depends, FastAPI, Request
from pydantic import BaseModel

from app import auth
from app.auth import authjwt_exception_handler
from app.settings import Settings
from app.routers import forms, sheet, user
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

app = FastAPI()

class authModel(BaseModel):
    authjwt_secret_key: str = Settings().secret_key

@AuthJWT.load_config
def get_config():
    return authModel()

app.add_exception_handler(AuthJWTException, authjwt_exception_handler)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/", tags=["info"], include_in_schema=False)
async def info():
    settings = Settings()
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "dbViewConn": settings.dbViewConn,
    }

app.include_router(auth.router)

app.include_router(user.router)
app.include_router(forms.router)
app.include_router(sheet.router)

