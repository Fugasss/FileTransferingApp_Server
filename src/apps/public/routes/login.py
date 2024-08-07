# https://fastapi.tiangolo.com/tutorial/bigger-applications/#apirouter

from src.apps.admin.database.DAOs.userDAO import get_all_users
from fastapi import APIRouter, Form
from typing import Annotated

router = APIRouter()


@router.post('/login')
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    users = get_all_users()

    for user in users:
        if user.check_login_password(username, password):
            return {"code": 0, "message": "Access accepted"}

    return {"code": 1, "message": "Access denied"}
