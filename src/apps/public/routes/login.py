# https://fastapi.tiangolo.com/tutorial/bigger-applications/#apirouter
import jwt
import src.apps.common.security.jwt as jwt_sec

from fastapi import APIRouter, Form
from typing import Annotated
from starlette.responses import JSONResponse
from src.apps.admin.database.DAOs.userDAO import get_user_by_login
from src.apps.admin.security.hasher import hash_password
from src.settings import JWT_SECRET_KEY, JWT_ALGORITHM

router = APIRouter()


@router.post('/login')
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    user = get_user_by_login(username)

    if user is None:
        return JSONResponse({"code": 404, "message": "User not found"})

    if user.password == hash_password(password, user.salt)[1]:
        try:
            payload = jwt_sec.Payload(username=user.login, password=user.password, group=user.group)
            key = JWT_SECRET_KEY
            algorithm = JWT_ALGORITHM
            token = jwt_sec.encode(
                payload=payload,
                key=key,
                algorithms=algorithm)
        except jwt.InvalidKeyError:
            return JSONResponse({"code": 400, "message": "Invalid Key"})
        except jwt.InvalidTokenError:
            return JSONResponse({"code": 400, "message": "Invalid Token"})
        except Exception as e:
            print(e)
            return JSONResponse({"code": 400, "message": str(e)})

        return JSONResponse({"code": 200, "message": "Login successful", 'token': token})
    else:
        return JSONResponse({"code": 403, "message": "Wrong password"})
