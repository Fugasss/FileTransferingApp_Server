from pydantic import BaseModel

from src.apps.admin.database.models.rights import Rights


class Group(BaseModel):
    id: int
    name: str
    rights: Rights
