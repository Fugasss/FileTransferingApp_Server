import jwt

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import src.apps.common.security.jwt as jwt_sec
from src.settings import JWT_SECRET_KEY, JWT_ALGORITHM


class JWTMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, *args, **kwargs):
        super().__init__(app)
        self.exclude_endpoints = kwargs['exclude_endpoints']

    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.exclude_endpoints:
            print('Ignoring jwt middleware')
            return await call_next(request)

        auth_header = request.headers.get('authorization')
        if auth_header:
            auth = auth_header.split(" ")
            if auth[0].lower() == "bearer":
                token = auth[1]
                try:
                    payload = jwt_sec.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
                    request.state.user = payload
                except jwt.ExpiredSignatureError:
                    raise HTTPException(status_code=401, detail="Token has expired")
                except jwt.InvalidTokenError:
                    raise HTTPException(status_code=401, detail="Invalid token")
        else:
            raise HTTPException(status_code=401, detail="Authorization header missing")

        response = await call_next(request)

        return response
