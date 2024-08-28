import dataclasses
import json
from datetime import datetime
from typing import Any, Dict

import jwt

from src.apps.admin.database.models.group import Group


@dataclasses.dataclass
class Payload:
    username: str
    password: str
    group: Group
    expires: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "username": self.username,
            "password": self.password,
            "group": {
                "id": str(self.group.id),
                "name": self.group.name,
                "rights": str(self.group.rights),
            },
            "expires": self.expires,
        }


def encode(payload: Payload,
           key: Any = "",
           algorithms: list[str] | None = None) -> str:
    data = payload.to_dict()
    return jwt.encode(data, key=key, algorithm=algorithms)


def decode(token: str,
           key: Any = "",
           algorithms: list[str] | None = None) -> Payload:
    data = jwt.decode(token, key=key, algorithms=algorithms)
    return Payload(**data)
