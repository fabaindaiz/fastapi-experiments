from functools import wraps
from typing import Optional
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException


class HTTP_400_BAD_REQUEST(HTTPException):
    """Used when the request is malformed"""
    def __init__(self, detail: Optional[str] = None):
        super().__init__(status.HTTP_400_BAD_REQUEST, detail)
    
class HTTP_401_UNAUTHORIZED(HTTPException):
    """Used when the user is not authenticated"""
    def __init__(self, detail: Optional[str] = None):
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail)
    
class HTTP_403_FORBIDDEN(HTTPException):
    """Used when the user tries to access a resource that he is not allowed to"""
    def __init__(self, detail: Optional[str] = None):
        super().__init__(status.HTTP_403_FORBIDDEN, detail)
    
class HTTP_404_NOT_FOUND(HTTPException):
    """Used when the requested resource is not found"""
    def __init__(self, detail: Optional[str] = None):
        super().__init__(status.HTTP_404_NOT_FOUND, detail)
    
class HTTP_408_REQUEST_TIMEOUT(HTTPException):
    """Used when the request takes too long to process"""
    def __init__(self, detail: Optional[str] = None):
        super().__init__(status.HTTP_408_REQUEST_TIMEOUT, detail)
    
class HTTP_500_INTERNAL_SERVER_ERROR(HTTPException):
    """Used when an unexpected error occurs"""
    def __init__(self, detail: Optional[str] = None):
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, detail)


def handleExceptions(func):
    """Decorator that handles all HTTP exceptions and returns a JSON response with the error message"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPException as exception:
            return JSONResponse(
                status_code = exception.status_code,
                content = jsonable_encoder({
                    "successful": False,
                    "message": exception.detail,
                })
            )
    return wrapper
