from typing import Annotated

from fastapi import Header, HTTPException


async def validate_header_auth(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
