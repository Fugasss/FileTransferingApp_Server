from fastapi import APIRouter, Form
from typing import Annotated

from src.apps.admin.database.DAOs.userDAO import create_user
from src.apps.admin.database.DAOs.groupDAO import get_group_by_name

router = APIRouter()


@router.post("/registration")
def register_user(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    print("register user")
    user, created = create_user(username, password, get_group_by_name("default"))
    print(user)
    if created:
        return {"code": 201, "message": "User registered successfully"}
    else:
        return {"code": 500, "message": "Something went wrong"}
