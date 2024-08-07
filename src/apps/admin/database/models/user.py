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


    def get_id(self) -> int:
        return self.id
    def get_group(self) -> Group:
        return self.group
    def get_login(self) -> str:
        return self.login

    def set_group(self, group: Group):
        self.group = group

    def check_login(self, login) -> bool:
        return login == self.login
    def check_password(self, password) -> bool:
        return password == self.password
    def check_login_password(self, login, password) -> bool:
        return self.check_login(login) and self.check_password(password)