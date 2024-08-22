from fastapi import APIRouter, Form
from typing import Annotated

from fastapi.responses import JSONResponse
from starlette import status

from src.apps.admin.database.DAOs.userDAO import create_user
from src.apps.admin.database.DAOs.groupDAO import get_group_by_name

router = APIRouter()


@router.post("/registration", status_code=status.HTTP_201_CREATED)
def register_user(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    user, created = create_user(username, password, get_group_by_name("default"))

    if created:
        return JSONResponse([{"message": "User created successfully"}])
    else:
        return JSONResponse([{"message": "User already exists"}])
