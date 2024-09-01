from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.apps.public.routes import login, files

allowed_origins = [
    '*'
]
public_app = FastAPI(description="Can be accessed from any origin",
                     title="Public API",
                     openapi_prefix="/public",)

public_app.add_middleware(CORSMiddleware,
                          allow_origins=allowed_origins,
                          allow_credentials=True,
                          allow_methods=["*"],
                          allow_headers=["*"])

public_app.include_router(login.router)
public_app.include_router(files.router)
