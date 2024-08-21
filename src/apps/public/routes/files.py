from fastapi import APIRouter, Query, File, UploadFile, Depends
from typing import Annotated, List
from fastapi.responses import FileResponse
from starlette.responses import JSONResponse
import shutil

from src.apps.common.database.utils import list_of_all_files, is_in_files, delete_file
from src.apps.common.dependencies import verify_jwt_token

router = APIRouter(
    prefix="/files",
    dependencies=[Depends(verify_jwt_token)],
)


FILES_PATH = "files/"


@router.get('/')
async def get_files(p: Annotated[int | None, Query(description="number of page")] = None):
    all_files = list_of_all_files(FILES_PATH)
    all_files.sort()

    if len(all_files) >= p * 20 and p is not None:
        return all_files[(p - 1) * 20:p * 20]
    else:
        return JSONResponse({"error": "No Files Found"}, status_code=404)


@router.get("/filename}")
async def download(filename: str):
    if is_in_files(filename, FILES_PATH):
        return FileResponse(path=FILES_PATH + filename)
    else:
        return JSONResponse({"error": "File Not Found"}, status_code=404)


@router.post('/upload')
async def upload_files(files: List[UploadFile] = File(...)):
    uploaded_files = []

    for file in files:
        path = FILES_PATH + file.filename

        with open(path, 'wb+') as buffer:
            shutil.copyfileobj(file.file, buffer)

        uploaded_files.append(file)

    return uploaded_files


@router.delete('/{filename}')
async def delete(filename: str):
    if delete_file(filename, FILES_PATH):
        return JSONResponse({"Success": filename + " was deleted"}, status_code=200)
    else:
        return JSONResponse({"Error": "File Not Found"}, status_code=404)