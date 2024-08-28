import dataclasses
from src.apps.admin.database.models.group import Group


@dataclasses.dataclass
class User:
    id: int
    login: str
    hashed_password: str
    salt: str
    group: Group
