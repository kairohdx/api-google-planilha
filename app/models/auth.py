from datetime import timedelta
from typing import Optional
from pydantic import BaseModel


class AuthBase(BaseModel):
    email:str = ''
    password:str = ''

class AuthResponse(BaseModel):
    access_token:str = "access_token"
    refresh_token:str = "refresh_token"
    expire_in: timedelta = timedelta(hours=3)

class AuthFlow(BaseModel):
    tokenUrl: str
    refreshUrl: Optional[str] = ''
    scopes: dict = {}

    class Config:
        extra = "allow"
        