import os

from datetime import datetime, timedelta

from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt

from ..models import Token, User

from api.schemas.token import TokenData

from passlib.context import CryptContext
from passlib.handlers.django import django_pbkdf2_sha256

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="tokens", scheme_name="JWT")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ACCESS_TOKEN_EXPIRE_DAYS = 60

def hash_password(password: str):
    return django_pbkdf2_sha256.hash(password)

def verify_password(password, encrypted_pasword):
    return django_pbkdf2_sha256.verify(password, encrypted_pasword)

async def get_user(username: str):
    return await User.objects.filter(username=username).afirst()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = "Null"):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se lograron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username == "Null":
            raise credentials_exception

        token = await Token.objects.filter(token=token).afirst()
        
        if not token:
            raise credentials_exception

        token_data = TokenData(username=username)
    except JWTError:
        if not token:
            raise credentials_exception
        try:
            token_temp = await Token.objects.filter(token=token).afirst()#TokenCRUD(db).get_token_by_token(token)
            if token_temp:
                await Token.objects.filter(token=token).adelete()
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tu token ha expirado, por favor inicia sesión nuevamente",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tu token ha expirado, por favor inicia sesión nuevamente",
                headers={"WWW-Authenticate": "Bearer"},
            )
    user = await get_user(username=token_data.username)
    if not user:
        raise credentials_exception

    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user
