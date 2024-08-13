from fastapi import APIRouter, File, UploadFile
from typing import List
import shutil

router = APIRouter()


@router.post('/upload')
async def upload_file(upload_file: UploadFile = File(...)):
    path = f'files/{upload_file.filename}'

    with open(path, 'wb+') as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return upload_file

@router.post('/multi-upload')
async def multiupload_file(upload_files: List[UploadFile] = File(...)):
    uploaded_files = []

    for upload_file in upload_files:
        path = f'files/{upload_file.filename}'

        with open(path, 'wb+') as buffer:
            shutil.copyfileobj(upload_file.file, buffer)

        uploaded_files.append(upload_file)

    return uploaded_files