﻿from src.apps.admin.database.models.user import User
from src.apps.admin.database.models.group import Group
from src.apps.admin.security import hasher
from src.apps.common.database.utils import execute_and_fetchall, execute_and_fetchone
from src.apps.common.database.connection import get_cursor
from src.apps.admin.database.DAOs.groupDAO import get_group_by_id
from src.apps.common.database.utils import read_sql_file


def get_all_users() -> tuple[User]:
    users: list[User] = []
    data = execute_and_fetchall('select_all_users.sql')

    for row in data:
        group = get_group_by_id(row[3])
        user = User(id=row[0], login=row[1], password=row[2], group=group)
        users.append(user)

    return tuple(*users)


def get_user_by_login(login) -> User | None:
    data = execute_and_fetchone('select_user_by_login.sql', (login,))

    if data is None:
        return None

    group = get_group_by_id(data[3])
    return User(id=data[0], login=data[1], password=data[2], group=group)


def create_user(login: str, password: str, group: Group) -> (User | None, bool):
    cursor = get_cursor()

    try:
        salt, hashed_password = hasher.hash_password(password)
        cursor.execute(read_sql_file('create_user.sql'), (login, hashed_password, salt, group.id))

    except Exception as e:
        print(e)
        return None, False

    else:
        return get_user_by_login(login), True

    finally:
        cursor.close()


def update_user(updated_user: User) -> bool:
    salt, hashed_password = hasher.hash_password(updated_user.password)
    updated_user.password = hashed_password

    params = updated_user.model_dump(exclude={'group'})
    params['salt'] = salt
    params['groupid'] = updated_user.group.id

    cursor = get_cursor()

    try:
        cursor.execute(read_sql_file('update_user.sql'), params)
    except Exception as e:
        print(e)
        return False
    else:
        return True


def delete_user(user: User) -> bool:
    cursor = get_cursor()

    try:
        cursor.execute(read_sql_file('delete_user.sql'), (user.id,))

    except Exception as e:
        print(e)
        return False

    else:
        return True

    finally:
        cursor.close()
