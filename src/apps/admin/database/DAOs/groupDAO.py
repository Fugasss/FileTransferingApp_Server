﻿from src.apps.admin.database.models.group import Group
from src.apps.common.database.db_utils import execute_and_fetchone, execute_and_fetchall
from src.apps.common.database.connection import get_cursor
from src.apps.common.database.utils import read_sql_file
from src.apps.admin.database.models.rights import Rights


def get_all_groups() -> tuple[Group, ...]:
    file = 'select_all_groups.sql'
    values = execute_and_fetchall(file)

    groups: list[Group] = []

    for row in values:
        groups.append(Group(id=row[0], name=row[1], rights=row[2]))

    return tuple(groups)


def get_group_by_id(group_id: int) -> Group | None:
    file = 'select_group_by_id.sql'
    params = (group_id,)
    value = execute_and_fetchone(file, params)

    if value is None:
        return None

    return Group(id=value[0], name=value[1], rights=value[2])


def get_group_by_name(name: str) -> Group | None:
    file = 'select_group_by_name.sql'
    params = (name,)
    value = execute_and_fetchone(file, params)

    if value is None:
        return None

    return Group(id=value[0], name=value[1], rights=value[2])


def create_group(name: str, rights: Rights) -> tuple[Group | None, bool]:
    file = 'create_group.sql'
    cursor = get_cursor()

    try:
        cursor.execute(read_sql_file(file), (name, rights))

    except Exception as e:
        print(e)
        return None, False

    else:
        return get_group_by_name(name), True

    finally:
        cursor.connection.commit()
        cursor.close()


def update_group(id: int, groupname: str, rights: str) -> bool:
    file = 'update_group.sql'
    params = (groupname, Rights(rights), id)

    cursor = get_cursor()

    try:
        cursor.execute(read_sql_file(file), params)
    except Exception as e:
        print(e)
        return False
    else:
        return True
    finally:
        cursor.connection.commit()
        cursor.close()


def delete_group_by_id(id: int) -> bool:
    file = 'delete_group_by_id.sql'
    cursor = get_cursor()

    try:
        cursor.execute(read_sql_file(file), (id,))

    except Exception as e:
        print(e)
        return False

    else:
        return True

    finally:
        cursor.connection.commit()
        cursor.close()


def delete_group_by_name(name: str) -> bool:
    file = 'delete_group_by_name.sql'
    cursor = get_cursor()

    try:
        cursor.execute(read_sql_file(file), (name,))

    except Exception as e:
        print(e)
        return False

    else:
        return True

    finally:
        cursor.connection.commit()
        cursor.close()
