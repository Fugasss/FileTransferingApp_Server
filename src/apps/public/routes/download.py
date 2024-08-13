from fastapi import APIRouter
from fastapi.responses import FileResponse


router = APIRouter()


@router.get("/download")
async def download(filename: str):
    return FileResponse(path="files/" + filename)