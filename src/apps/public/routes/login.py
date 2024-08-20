# https://fastapi.tiangolo.com/tutorial/bigger-applications/#apirouter
import time

import jwt
from starlette.requests import Request
from starlette.responses import Response

import src.apps.common.security.jwt as jwt_sec

from fastapi import APIRouter, Form
from typing import Annotated, Optional
from starlette.responses import JSONResponse
from src.apps.admin.database.DAOs.userDAO import get_user_by_login
from src.apps.admin.security.hasher import hash_password
from src.settings import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_TOKEN_EXPIRE

router = APIRouter()


@router.post('/login')
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    user = get_user_by_login(username)

    if user is None:
        return JSONResponse({"message": "User not found"}, status_code=404)

    if user.password == hash_password(password, user.salt)[1]:
        try:
            payload = jwt_sec.Payload(username=user.login,
                                      password=user.password,
                                      group=user.group,
                                      expires=(time.time() + JWT_TOKEN_EXPIRE))
            key = JWT_SECRET_KEY
            algorithm = JWT_ALGORITHM
            token = jwt_sec.encode(
                payload=payload,
                key=key,
                algorithms=algorithm)
        except jwt.InvalidKeyError:
            return JSONResponse({"code": 400, "message": "Invalid Key"}, status_code=400)
        except jwt.InvalidTokenError:
            return JSONResponse({"code": 400, "message": "Invalid Token"}, status_code=400)
        except Exception as e:
            print(e)
            return JSONResponse({"code": 400, "message": str(e)}, status_code=400)

        return JSONResponse({"code": 200, "message": "Login successful", 'token': token}, status_code=200)
    else:
        return JSONResponse({"code": 403, "message": "Wrong password"}, status_code=403)
