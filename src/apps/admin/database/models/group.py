from pydantic import BaseModel

from src.apps.admin.database.models.rights import Rights


class Group(BaseModel):
    id: int
    name: str
    rights: Rights

    def __init__(self, id, name, rights):
        super().__init__()
        self.id = id
        self.name = name
        self.rights = rights
