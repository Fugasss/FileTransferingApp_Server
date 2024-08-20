from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

from src.apps.admin.database.models.rights import Rights
from src.apps.admin.routes import login, registration, users, groups
from src.apps.common.middlewares.JWTMiddleware import JWTMiddleware

allowed_origins = [
    "http://localhost:5173",
    "https://localhost:5173",
]

admin_app = FastAPI(description="Can be accessed only from local machine", title="Admin API")

admin_app.add_middleware(CORSMiddleware,
                         allow_origins=allowed_origins,
                         allow_credentials=True,
                         allow_methods=["*"],
                         allow_headers=["*"])


admin_app.include_router(login.router)
admin_app.include_router(registration.router)
admin_app.include_router(users.router)
admin_app.include_router(groups.router)


# @admin_app.middleware('http')
# async def check_access_rights(request: Request, call_next):
#     if request.user.group.rights != Rights.FULL:
#         print(f'User {request.user.login} has no rights to access this app')
#         raise HTTPException(status_code=403, detail='User does not have rights to access this app')
# 
#     return await call_next(request)
