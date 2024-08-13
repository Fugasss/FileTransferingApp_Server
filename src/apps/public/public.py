﻿from fastapi import FastAPI

from src.apps.public.routes import login, upload, download

public_app = FastAPI(description="Can be accessed from any origin", title="Public API")

public_app.include_router(login.router)
public_app.include_router(upload.router)
public_app.include_router(download.router)