
from pydantic import BaseModel

class UpdateModel(BaseModel):
    class Config:
        extra = "forbid"

class Persona(UpdateModel):
    nombre: str
    edad: int