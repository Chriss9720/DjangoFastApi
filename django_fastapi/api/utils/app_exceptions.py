from fastapi import Request
from starlette.responses import JSONResponse

class AppExceptionCase(Exception):
    def __init__(self, status_code: int, context: dict):
        self.exception_case = self.__class__.__name__
        self.status_code = status_code
        self.context = context

    def __str__(self):
        return (
            f"<AppException {self.exception_case} - "
            + f"status_code={self.status_code} - context={self.context}>"
        )


async def app_exception_handler(request: Request, exc: AppExceptionCase):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "app_exception": exc.exception_case,
            "context": exc.context,
        },
    )

class AppException(object):

    class FooCreateItem(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Item creation failed
            """
            status_code = 500
            AppExceptionCase.__init__(self, status_code, context)
    
    class FooUpdateItem(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Item update failed
            """
            status_code = 500
            AppExceptionCase.__init__(self, status_code, context)
    
    class FooDeleteItem(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Item delete failed
            """
            status_code = 500
            AppExceptionCase.__init__(self, status_code, context)

    class FooGetItem(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Item not found
            """
            status_code = 404
            AppExceptionCase.__init__(self, status_code, context)
    
    class FooGetAll(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Item not found
            """
            status_code = 404
            AppExceptionCase.__init__(self, status_code, context)

    class FooItemRequiresAuth(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Item is not public and requires auth
            """
            status_code = 401
            AppExceptionCase.__init__(self, status_code, context)

    class GetUser(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            User not found
            """
            status_code = 404
            AppExceptionCase.__init__(self, status_code, context)

    class GetAllUser(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Users not found
            """
            status_code = 404
            AppExceptionCase.__init__(self, status_code, context)

    class CreateUser(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            User creation failed
            """
            status_code = 404
            AppExceptionCase.__init__(self, status_code, context)

    class UpdateUser(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            User update failed
            """
            status_code = 404
            AppExceptionCase.__init__(self, status_code, context)
    
    class DeleteUser(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            User delete failed
            """
            status_code = 404
            AppExceptionCase.__init__(self, status_code, context)

    class CreateToken(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Token creation failed
            """
            status_code = 500
            AppExceptionCase.__init__(self, status_code, context)
    
    class GetToken(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Token not found
            """
            status_code = 404
            AppExceptionCase.__init__(self, status_code, context)

    class TokenInvalidCredentials(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Token invalid
            """
            status_code = 404
            AppExceptionCase.__init__(self, status_code, context)