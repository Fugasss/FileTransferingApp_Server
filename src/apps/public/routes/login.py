# https://fastapi.tiangolo.com/tutorial/bigger-applications/#apirouter

from fastapi import APIRouter, Form
from typing import Annotated

router = APIRouter()


@router.post('/login')
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    # check if user exists
    # check password

    return {"code": 403, "message": "Access denied"}
