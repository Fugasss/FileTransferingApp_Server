import os.path

from fastapi import APIRouter, Query, File, UploadFile, Depends, HTTPException
from typing import Annotated, List
from fastapi.responses import FileResponse, JSONResponse, Response
import shutil

from src.settings import FILES_DIR
from src.apps.common.database.utils import list_of_all_files, is_in_files, delete_file
from src.apps.common.dependencies import verify_jwt_token
from src.apps.admin.database.models.filelist import FileList

router = APIRouter(
    prefix="/files",
    dependencies=[Depends(verify_jwt_token)],
)


@router.get('/page')
async def get_files(p: Annotated[int | None, Query(description="number of page")] = None):
    all_files = list_of_all_files(FILES_DIR)
    all_files.sort()

    if p is not None and len(all_files) >= p * 20:
        return JSONResponse(all_files[(p - 1) * 20:p * 20], status_code=200)
    elif len(all_files) > 0:
        return JSONResponse(all_files, status_code=200)
    else:
        raise HTTPException(status_code=404)


@router.get('/')
async def get_all_files():
    return sorted(list_of_all_files(FILES_DIR))


@router.get("/{filename}")
async def download(filename: str):
    if is_in_files(filename, FILES_DIR):
        return FileResponse(path=os.path.join(FILES_DIR, filename))
    else:
        raise HTTPException(status_code=404, detail='File not found')


@router.post('/upload')
async def upload_files(files: List[UploadFile] = File(...)):
    uploaded_files = []

    for file in files:
        path = os.path.join(FILES_DIR, file.filename)

        with open(path, 'wb+') as buffer:
            shutil.copyfileobj(file.file, buffer)

        uploaded_files.append(file)

    return uploaded_files


@router.delete('/{filename}')
async def delete(filename: str):
    if delete_file(filename, FILES_DIR):
        return Response(status_code=200)
    else:
        raise HTTPException(status_code=404, detail='File not found')


@router.delete('/')
async def delete_files(file_list: FileList):
    not_found_files = []

    for filename in file_list.filenames:
        if not delete_file(filename, FILES_DIR):
            not_found_files.append(filename)

    if not_found_files:
        raise HTTPException(status_code=404, detail=f"Files not found: {', '.join(not_found_files)}")

    return Response(status_code=200)