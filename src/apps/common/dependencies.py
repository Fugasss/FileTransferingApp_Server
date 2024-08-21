import time
import jwt

from fastapi import HTTPException, Depends, Header
from starlette import status
from typing import Annotated

from src.apps.admin.database.DAOs import userDAO as usersDB
from src.apps.admin.database.models.rights import Rights
from src.apps.admin.database.models.user import User
from src.apps.admin.security import hasher
from src.settings import JWT_SECRET_KEY, JWT_ALGORITHM

import src.apps.common.security.jwt as jwt_sec


def verify_password(password: str, hashed_password: str) -> bool:
    return password == hashed_password


def authenticate_user(username: str, password: str) -> User:
    user = usersDB.get_user_by_login(username)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect password')

    return user


def verify_jwt_token(authorization: Annotated[str, Header()]) -> User:
    auth = authorization.split(" ")
    if auth[0].lower() == "bearer":
        token = auth[1]
        try:
            payload = jwt_sec.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])

            if time.time() >= payload.expires:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
            else:
                return authenticate_user(payload.username, payload.password)

        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong authorization")


def verify_full_rights(user: Annotated[User, Depends(verify_jwt_token)]):
    if user.group.rights != Rights.FULL:
        raise HTTPException(status_code=403, detail='User does not have rights to access this route')
