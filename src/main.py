from fastapi import FastAPI

from src.apps.admin.admin import admin_app
from src.apps.public.public import public_app
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

app = FastAPI()

app.mount('/admin', admin_app)
app.mount('/', public_app)
