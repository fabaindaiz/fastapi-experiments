from fastapi import APIRouter
from fastapi import Depends
from functools import wraps
from src.exceptions import *

router = APIRouter(
    tags=["wrapper"],
    prefix="/wrapper",
)


# Example 1: Applying a verification in a decorator capturing the user from the kwargs
def get_user():
    return {"name": "test", "permissions": ["test"]}

def permissions(permissions: list[str]):
    def aux(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user = kwargs.get("user", None)
            if not user:
                raise HTTP_401_UNAUTHORIZED("No está autenticado")
            for permission in permissions:
                if permission not in user["permissions"]:
                    raise HTTP_403_FORBIDDEN("No tiene permisos")
            return await func(*args, **kwargs)
        return wrapper
    return aux

@router.get("/test1")
@handleExceptions
@permissions(["test"])
async def test1(user = Depends(get_user)):
    return user


# Example 2: Abstracting the user capture from the kwargs allowing to simplify the verification
def inject_permissions(verfication):
    def aux(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if not "user" in kwargs:
                raise HTTP_401_UNAUTHORIZED("No está autenticado")
            verfication(kwargs["user"])
            return await func(*args, **kwargs)
        return wrapper
    return aux

def names(names: list[str]):
    @inject_permissions
    def verification(user):
        if user["name"] not in names:
            raise HTTP_403_FORBIDDEN("No tiene permisos")
    return verification

def permissions(permissions: list[str]):
    @inject_permissions
    def verification(user):
        for permission in permissions:
            if permission not in user["permissions"]:
                raise HTTP_403_FORBIDDEN("No tiene permisos")
    return verification

@router.get("/test2")
@handleExceptions
@names(["test"])
@permissions(["test"])
async def test2(user = Depends(get_user)):
    return user
