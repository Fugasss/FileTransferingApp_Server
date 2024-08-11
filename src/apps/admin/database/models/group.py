import dataclasses
from src.apps.admin.database.models.rights import Rights


@dataclasses.dataclass
class Group:
    id: int
    name: str
    rights: Rights
