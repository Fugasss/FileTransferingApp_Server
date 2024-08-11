from typing import Annotated

from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse

router = APIRouter()
router.default_response_class = JSONResponse


@router.post('/login')
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    pass
