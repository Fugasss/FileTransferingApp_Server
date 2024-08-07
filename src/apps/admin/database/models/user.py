from pydantic import BaseModel

from src.apps.admin.database.models.group import Group


class User(BaseModel):
    id: int
    login: str
    password: str
    group: Group

    def __init__(self, id, login, password, group):
        super().__init__()
        self.id = id
        self.login = login
        self.password = password
        self.group = group
