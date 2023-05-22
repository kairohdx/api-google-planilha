from pydantic import BaseModel


class UserBase(BaseModel):
    name: str = ''
    email: str = ''
    scope: str = 'private'

class UserPost(UserBase):
    passHash: str = ''

class UserLogin(BaseModel):
    email: str = ''
    passHash: str = ''
    scope: str = ''
