from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from src.apps.common.database.connection import get_cursor
from src.apps.common.database.utils import read_sql_file
from fastapi import File, UploadFile, HTTPException

router = APIRouter()


@router.post('/upload')
async def upload_file(file: UploadFile = File(...)):
    cursor = get_cursor()
    try:
        file_data = await file.read()
        cursor.execute(read_sql_file('create_file.sql'), (file.filename, file.size, file_data))

        file_id = cursor.lastrowid
        return ORJSONResponse([{"message": "file uploaded successfully", "file_id": file_id}])

    except Exception as e:
        raise HTTPException(status_code=500, detail="File upload failed") from e

    finally:
        cursor.close()
