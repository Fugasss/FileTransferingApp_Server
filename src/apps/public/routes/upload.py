from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from typing import List
import shutil

from src.apps.common.database.connection import get_cursor
from src.apps.common.database.utils import read_sql_file

router = APIRouter()


@router.post('/upload')
async def upload_file(upload_file: UploadFile = File(...)):
    path = f'files/{upload_file.filename}'

    with open(path, 'wb+') as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return {'path': path}