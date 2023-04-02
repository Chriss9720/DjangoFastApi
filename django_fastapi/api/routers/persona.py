from fastapi import APIRouter, Depends, Request

from ..utils.service_result import handle_result
from ..utils.auth import get_current_user

from slowapi import Limiter
from slowapi.util import get_remote_address

from ..schemas.user import User
from ..schemas.request import Persona

from ..services.personas import PersonaService

limiter = Limiter(key_func=get_remote_address)

router = APIRouter(
    prefix="/personas",
    tags=["personas"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
@limiter.limit("6000/minute")
async def create(request: Request, item: Persona, current_user: User = Depends(get_current_user)):
    persona = await PersonaService().create(item, current_user)
    return handle_result(persona)

@router.get("/{name}")
async def get(request: Request, name: str, current_user: User = Depends(get_current_user)):
    persona = await PersonaService().get_by_name(name, current_user)
    return handle_result(persona)

@router.delete("/{name}")
async def get(request: Request, name: str, current_user: User = Depends(get_current_user)):
    persona = await PersonaService().deleted(name, current_user)
    return handle_result(persona)

@router.put("/{name}")
async def get(request: Request, name: str, item: Persona, current_user: User = Depends(get_current_user)):
    persona = await PersonaService().update(name, item, current_user)
    return handle_result(persona)