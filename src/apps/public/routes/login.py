# https://fastapi.tiangolo.com/tutorial/bigger-applications/#apirouter
import time
from datetime import timedelta

import jwt
from starlette.requests import Request
from starlette.responses import Response

import src.apps.common.security.jwt as jwt_sec

from fastapi import APIRouter, Form, HTTPException
from typing import Annotated, Optional
from starlette.responses import JSONResponse
from src.apps.admin.database.DAOs.userDAO import get_user_by_login
from src.apps.admin.database.models.user import User
from src.apps.admin.security.hasher import hash_password
from src.settings import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_TOKEN_EXPIRE_SECONDS

router = APIRouter()


def verify_password(plain_password: str, hashed_password: str, salt: str) -> bool:
    return hash_password(plain_password, salt)[1] == hashed_password


def create_access_token(user: User, expires_delta: Optional[float] = None):
    payload = jwt_sec.Payload(username=user.login,
                              password=user.hashed_password,
                              group=user.group,
                              expires=(time.time() + expires_delta))
    key = JWT_SECRET_KEY
    algorithm = JWT_ALGORITHM
    token = jwt_sec.encode(
        payload=payload,
        key=key,
        algorithms=algorithm)

    return token


@router.post('/login')
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    user = get_user_by_login(username)

    if user is None:
        return JSONResponse({"message": "User not found"}, status_code=404)

    if verify_password(password, user.hashed_password, user.salt):
        try:
            token = create_access_token(user, JWT_TOKEN_EXPIRE_SECONDS)
        except jwt.InvalidKeyError:
            raise HTTPException(status_code=400, detail="Invalid Key")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=400, detail="Invalid Token")
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

        return JSONResponse({"message": "Login successful", 'token': token, 'jwt_exp_seconds': str(JWT_TOKEN_EXPIRE_SECONDS)}, status_code=200)
    else:
        raise HTTPException(status_code=403, detail='Wrong Credentials')
