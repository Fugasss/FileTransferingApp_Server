import dataclasses
from src.apps.admin.database.models.group import Group


@dataclasses.dataclass
class User:
    id: int
    login: str
    password: str
    salt: str
    group: Group
