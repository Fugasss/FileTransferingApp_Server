from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.apps.admin.admin import admin_app
from src.apps.common.database.connection import get_cursor, close_connection
from src.apps.public.public import public_app


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_cursor().close()

    yield

    close_connection()

description = f"## Welcome to the FTA\nHere are links to the documentation of sub-applications:\n- [Admin](http://localhost:8080/admin/docs)\n- [Public](http://localhost:8080/public/docs)"

app = FastAPI(lifespan=lifespan,
              version='1.0.0',
              title="FTA's docs",
              description=description,
              )

app.mount('/admin', admin_app)
app.mount('/', public_app)
app.mount('/files', StaticFiles(directory='files'), name='files')