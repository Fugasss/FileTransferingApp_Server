from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.apps.admin.admin import admin_app
from src.apps.common.database.connection import get_cursor, close_connection
from src.apps.common.middlewares.JWTMiddleware import JWTMiddleware
from src.apps.public.public import public_app
from dotenv import load_dotenv


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_cursor().close()

    yield

    close_connection()


app = FastAPI(lifespan=lifespan)

app.mount('/admin', admin_app)
app.mount('/', public_app)
app.mount('/files', StaticFiles(directory='files'), name='files')

app.add_middleware(JWTMiddleware, exclude_endpoints=['/admin/registration', '/login'])
