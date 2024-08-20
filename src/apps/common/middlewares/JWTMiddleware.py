import time
from datetime import datetime

import jwt

from fastapi import Request, HTTPException
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, JSONResponse

import src.apps.common.security.jwt as jwt_sec
from src.settings import JWT_SECRET_KEY, JWT_ALGORITHM


class JWTMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, *args, **kwargs):
        super().__init__(app)
        self.exclude_endpoints = kwargs['exclude_endpoints']

    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.exclude_endpoints:
            return await call_next(request)

        if request.method == 'OPTIONS':
            return await call_next(request)

        auth_header = request.headers.get('authorization')
        if auth_header:
            auth = auth_header.split(" ")
            if auth[0].lower() == "bearer":
                token = auth[1]
                try:
                    payload = jwt_sec.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])

                    if time.time() >= payload.expires:
                        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                                            content={'message': 'Token is expired'})

                    request.state.user = payload
                except jwt.ExpiredSignatureError:
                    return Response(status_code=status.HTTP_401_UNAUTHORIZED, media_type='application/json',
                                    content={'message': 'Token is expired'})
                except jwt.InvalidTokenError:
                    return Response(status_code=status.HTTP_401_UNAUTHORIZED, media_type='application/json',
                                    content={'message': 'Invalid token'})
        else:
            return Response(status_code=status.HTTP_401_UNAUTHORIZED, media_type='application/json',
                            content={'message': 'Authorization header is missing'})

        response = await call_next(request)

        return response
