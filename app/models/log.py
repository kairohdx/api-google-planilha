from pydantic import BaseModel


class Log(BaseModel):
    path:str | None = None
    error:str | None = None
    statusCode: str | None
