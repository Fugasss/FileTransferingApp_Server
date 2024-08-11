from pydantic import BaseModel

from src.apps.admin.database.models.group import Group


class User(BaseModel):
    id: int
    login: str
    password: str
    salt: str
    group: Group
