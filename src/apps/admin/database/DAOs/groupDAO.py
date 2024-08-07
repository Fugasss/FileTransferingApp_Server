from src.apps.admin.database.models.group import Group
from src.apps.common.database.utils import execute_and_fetchone, execute_and_fetchall


def get_all_groups() -> tuple[Group]:
    file = './SQL/select_group_by_id.sql'
    values = execute_and_fetchall(file)

    groups: list[Group] = []

    for row in values:
        groups.append(Group(id=row[0], name=row[1], rights=row[2]))

    return tuple(*groups)


def get_group_by_id(group_id) -> Group | None:
    file = './SQL/select_group_by_id.sql'
    params = (group_id,)
    value = execute_and_fetchone(file, params)

    if value is None:
        return None

    return Group(id=value[0], name=value[1], rights=value[2])
