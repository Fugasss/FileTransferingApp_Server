from fastapi import APIRouter, Form
from typing import Annotated

from fastapi.responses import ORJSONResponse
from starlette import status

from src.apps.admin.database.DAOs.userDAO import create_user
from src.apps.admin.database.DAOs.groupDAO import get_group_by_name

router = APIRouter()
router.default_response_class = ORJSONResponse


@router.post("/registration", status_code=status.HTTP_201_CREATED)
def register_user(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    user, created = create_user(username, password, get_group_by_name("default"))

    if created:
        return ORJSONResponse([{"message": "User created successfully"}])

    return ORJSONResponse([{"message": "User already exists"}])
