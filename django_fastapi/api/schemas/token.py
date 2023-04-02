from os import access
from typing import Optional
from pydantic import BaseModel

class TokenData(BaseModel):
    username: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True

class OpenAPIToken(BaseModel):
    access_token: str

    class Config:
        orm_mode = True