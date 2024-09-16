from pydantic import BaseModel
from typing import List

class FileList(BaseModel):
    filenames: List[str]