import inspect
from typing import Callable
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
    def wrapper(endpoint: Callable):
        @wraps(endpoint)
        async def inner(*args, **kwargs):
            user = kwargs.get("user", None)
            if not user:
                raise HTTP_401_UNAUTHORIZED("No está autenticado")
            for permission in permissions:
                if permission not in user["permissions"]:
                    raise HTTP_403_FORBIDDEN("No tiene permisos")
            return await endpoint(*args, **kwargs)
        return inner
    return wrapper

@router.get("/test1")
@handleExceptions
@permissions(["test"])
async def test1(user = Depends(get_user)):
    return user


# Example 2: Abstracting the user capture from the kwargs allowing to simplify the verification
def _get_params(verification, endpoint):
    required = inspect.signature(verification).parameters.keys()
    params = inspect.signature(endpoint).parameters.keys()
    missing = list(set(required) - set(params))
    if not missing:
        return required
    raise Exception(f"In endpoint {endpoint.__name__} the function {verification.__name__} requires the parameters {missing}")

def inject_depends(verification: Callable):
    @wraps(verification)
    def wrapper(endpoint: Callable):
        params = _get_params(verification, endpoint)
        @wraps(endpoint)
        async def inner(*args, **kwargs):
            parameters = {key: kwargs[key] for key in params}
            if await verification(**parameters):
                return await endpoint(*args, **kwargs)
            raise HTTP_403_FORBIDDEN("You are not authorized to do this operation")
        return inner
    return wrapper


def names(names: list[str]):
    @inject_depends
    async def verification(user):
        if user["name"] in names:
            return True
        raise HTTP_403_FORBIDDEN("No tiene permisos")
    return verification

def permissions(permissions: list[str]):
    @inject_depends
    async def verification(user):
        for permission in permissions:
            if permission not in user["permissions"]:
                raise HTTP_403_FORBIDDEN("No tiene permisos")
        return True
    return verification

@router.get("/test2")
@handleExceptions
@names(["test"])
@permissions(["test"])
async def test2(user = Depends(get_user)):
    return user
