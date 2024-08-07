from fastapi import FastAPI

from src.apps.public.routes import login

public_app = FastAPI(description="Can be accessed from any origin", title="Public API")

public_app.include_router(login.router)
