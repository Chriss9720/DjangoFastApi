from pydantic import BaseModel, constr

class Credential(BaseModel):
    username: str
    password: str

class UserData(BaseModel):
    first_name : str
    last_name : str
    email : str
    rfc : constr(min_length=13, max_length=14)
    curp : str

class User(UserData):
    id: int

    class Config:
        orm_mode = True

class UserCreate(UserData):
    username: str
    password: str