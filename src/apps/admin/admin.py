from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.apps import admin
from src.apps.admin.routes import login, registration
from src.apps.admin.routes import upload


allowed_origins = [
    "https://localhost",
    "https://localhost:8000",
    "http://localhost",
    "http://localhost:8000",
]

admin_app = FastAPI(description="Can be accessed only from local machine", title="Admin API")

admin_app.add_middleware(CORSMiddleware,
                         allow_origins=allowed_origins,
                         allow_credentials=True,
                         allow_methods=["*"],
                         allow_headers=["*"])
admin_app.include_router(login.router)
admin_app.include_router(registration.router)
admin_app.include_router(upload.router)
