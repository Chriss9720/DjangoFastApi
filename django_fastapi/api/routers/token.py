from fastapi import APIRouter, Depends

from ..schemas.token import Token
from ..schemas.user import Credential

from ..services.token import TokenService

from fastapi.security import OAuth2PasswordRequestForm

from ..utils.service_result import handle_result

router = APIRouter(
    prefix="/tokens",
    tags=["Tokens"],
    responses={404: {"description": "Not found"}},
)

@router.post("", response_model=Token)
async def open_api_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = Credential(username = form_data.username, password = form_data.password)
    result = await TokenService().create_token(user)
    return handle_result(result)
