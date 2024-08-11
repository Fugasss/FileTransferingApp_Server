# https://fastapi.tiangolo.com/tutorial/bigger-applications/#apirouter

from fastapi import APIRouter, Form
from typing import Annotated
from src.apps.admin.database.DAOs.userDAO import get_user_by_login
from src.apps.admin.security.hasher import hash_password

router = APIRouter()


@router.post('/login')
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    print("login user")
    user = get_user_by_login(username)

    if user is None:
        return {"code": 404, "message": "User not found"}

    if user.password == hash_password(password, user.salt)[1]:
        return {"code": 200, "message": "Login successful"}
    else:
        return {"code": 403, "message": "Access denied"}
