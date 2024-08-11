from typing import Annotated

from fastapi import APIRouter, Form

router = APIRouter()


@router.post('/login')
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    pass
