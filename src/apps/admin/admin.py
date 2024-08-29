from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from src.apps.admin.routes import registration, users, groups
from src.apps.common.dependencies import verify_jwt_token, verify_full_rights

allowed_origins = [
    "http://localhost:5173",
    "https://localhost:5173",
]

admin_app = FastAPI(
    description="Can be accessed only from local machine",
    title="Admin API",
    dependencies=[Depends(verify_jwt_token), Depends(verify_full_rights)],
    openapi_prefix="/admin",
)


admin_app.add_middleware(CORSMiddleware,
                         allow_origins=allowed_origins,
                         allow_credentials=True,
                         allow_methods=["*"],
                         allow_headers=["*"])


admin_app.include_router(registration.router)
admin_app.include_router(users.router)
admin_app.include_router(groups.router)