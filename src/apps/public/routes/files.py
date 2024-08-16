from fastapi import APIRouter, Query,  File, UploadFile
from typing import Annotated, List
from fastapi.responses import FileResponse
from starlette.responses import JSONResponse
import shutil

from src.apps.common.database.utils import list_of_all_files, is_in_files, delete_file

router = APIRouter()


files_path = "files/"


@router.get('/files')
async def get_files(p: Annotated[int | None, Query(description="number of page")] = None):
    all_files = list_of_all_files(files_path)
    all_files.sort()

    if len(all_files) >= p * 20 and p is not None:
        return all_files[(p - 1) * 20:p * 20]
    else:
        return JSONResponse({"error": "No Files Found"}, status_code=404)


@router.get("/files/{filename}")
async def download(filename: str):
    if is_in_files(filename, files_path):
        return FileResponse(path=files_path + filename)
    else:
        return JSONResponse({"error": "File Not Found"}, status_code=404)


@router.post('/files/upload')
async def upload_files(upload_files: List[UploadFile] = File(...)):
    uploaded_files = []

    for upload_file in upload_files:
        path = files_path + upload_file.filename

        with open(path, 'wb+') as buffer:
            shutil.copyfileobj(upload_file.file, buffer)

        uploaded_files.append(upload_file)

    return uploaded_files


@router.delete('/files/{filename}')
async def delete(filename: str):
    if delete_file(filename, files_path):
        return JSONResponse({"Success": filename + " was deleted"}, status_code=200)
    else:
        return JSONResponse({"Error": "File Not Found"}, status_code=404)