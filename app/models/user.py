from pydantic import BaseModel

class UserBase(BaseModel):
    name: str = ''
    email: str = ''


class UserPost(UserBase):
    passHash: str = ''

class UserLogin(BaseModel):
    email: str = ''
    passHash: str = ''
