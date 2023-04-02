from datetime import timedelta

from ..schemas.token import Token
from ..schemas.user import Credential as User

from ..models import User
from ..models import Token as TokenDB

from ..utils.app_exceptions import AppException
from ..utils.service_result import ServiceResult
from ..utils.auth import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_DAYS

class TokenService:

    async def create_token(self, user: User) -> ServiceResult:

        exist = await User.objects.filter(username=user.username).afirst()

        if not exist:
            return ServiceResult(AppException.GetToken({"Message": "Incorrect username or password"}))

        is_logged = verify_password(user.password, exist.password)

        if not is_logged:
            return ServiceResult(AppException.TokenInvalidCredentials({"Message": "Incorrect username or password"}))

        access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)

        token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

        token = await TokenDB.objects.acreate(user_id = exist.id, token = token, created_by_id = exist.id)
        
        if not token:
            return ServiceResult(AppException.CreateToken({"Message": "Incorrect username or password"}))

        token = Token(access_token=token.token, token_type="Bearer")

        return ServiceResult(token)