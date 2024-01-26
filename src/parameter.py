from functools import wraps
from typing import Callable
from fastapi import APIRouter
from fastapi import Depends
from src.exceptions import *

router = APIRouter(
    tags=["parameter"],
    prefix="/parameter",
)

def depends_wrapper(func):
    """Decorator that wrapps a function with arguments inside a function without arguments"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        def aux():
            return func(*args, **kwargs)
        return aux
    return wrapper


# Example 1: Passing a function with arguments as a dependency
@depends_wrapper
def print_wrapped(text: str):
    print(text)

def print_unwrapped(text: str):
    print(text)

@router.get("/test1")
async def test1(user=Depends(print_wrapped("test"))):
    return True

# user=Depends(print_wrapped("test"))
# This line is equivalent to:
depends_wrapper(print_unwrapped)("example")()


# Example 2: Making a function that verifies if the user has permissions
def get_user():
    return {"name": "test", "permissions": ["test"]}

@depends_wrapper
def has_permissions(user_fun: Callable, permissions: list = []):
    """Function that checks if the user has the permissions"""
    user = user_fun()
    for permission in permissions:
        if permission not in user["permissions"]:
            raise PermissionError("No tiene permisos")
    return user

@router.get("/test2")
async def test2(user=Depends(has_permissions(get_user, ["test"]))):
    return user


# Example 3: Making a function that applies a list of verifications to a user
@depends_wrapper
def apply_verification(user_fun: Callable, verifications: list[Callable]):
    """Function that applies a list of verifications to a user"""
    user = user_fun()
    for verification in verifications:
        if not verification(user):
            raise PermissionError("No tiene permisos")
    return user

def has_permissions(permissions: list = []):
    """Function that checks if the user has the permissions"""
    def aux(user):
        for permission in permissions:
            if permission not in user["permissions"]:
                return False
        return True
    return aux

@router.get("/test3")
@handleExceptions
def test3(user=Depends(apply_verification(get_user, [has_permissions(["test"])]))):
    return user
