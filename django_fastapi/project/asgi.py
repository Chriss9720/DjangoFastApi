import os

from django.apps import apps
from django.conf import settings
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

apps.populate(settings.INSTALLED_APPS)

from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from starlette.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import RequestValidationError

from api.routers import token, persona

from starlette.exceptions import HTTPException as StarletteHTTPException

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from api.utils.app_exceptions import AppExceptionCase
from api.utils.request_exceptions import (
    http_exception_handler,
    request_validation_exception_handler,
)
from api.utils.app_exceptions import app_exception_handler

def get_application() -> FastAPI:

    app = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.state.limiter = Limiter(key_func=get_remote_address)

    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    @app.exception_handler(StarletteHTTPException)
    async def custom_http_exception_handler(request, e):
        return await http_exception_handler(request, e)

    @app.exception_handler(RequestValidationError)
    async def custom_validation_exception_handler(request, e):
        return await request_validation_exception_handler(request, e)

    @app.exception_handler(AppExceptionCase)
    async def custom_app_exception_handler(request, e):
        return await app_exception_handler(request, e)

    app.include_router(token.router)
    app.include_router(persona.router)

    app.mount("/django", WSGIMiddleware(get_wsgi_application()))

    return app

app = get_application()
