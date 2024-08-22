from src.apps.admin.database.models.user import User
from src.apps.admin.database.models.group import Group
from src.apps.admin.security import hasher
from src.apps.common.database.db_utils import execute_and_fetchone, execute_and_fetchall
from src.apps.common.database.connection import get_cursor
from src.apps.admin.database.DAOs.groupDAO import get_group_by_id, get_group_by_name
from src.apps.common.database.utils import read_sql_file


def get_all_users() -> tuple[User, ...]:
    file = 'select_all_users.sql'

    users: list[User] = []
    data = execute_and_fetchall(file)

    for row in data:
        group = get_group_by_id(row[4])
        user = User(id=row[0], login=row[1], hashed_password=row[2], salt=row[3], group=group)
        users.append(user)

    return tuple(users)


def get_user_by_login(login) -> User | None:
    file = 'select_user_by_login.sql'
    params = (login,)

    data = execute_and_fetchone(file, params)

    if data is None:
        return None

    group = get_group_by_id(data[4])
    return User(id=data[0], login=data[1], hashed_password=data[2], salt=data[3], group=group)


def get_user_by_id(id) -> User | None:
    file = 'select_user_by_id.sql'
    params = (id,)

    data = execute_and_fetchone(file, params)

    if data is None:
        return None

    group = get_group_by_id(data[4])
    return User(id=data[0], login=data[1], hashed_password=data[2], salt=data[3], group=group)


def create_user(login: str, password: str, group: Group) -> (User | None, bool):
    file = 'create_user.sql'

    cursor = get_cursor()

    try:
        salt, hashed_password = hasher.hash_password(password)
        cursor.execute(read_sql_file(file), (login, hashed_password, salt, group.id))

    except Exception as e:
        print(e)
        return None, False

    else:
        return get_user_by_login(login), True

    finally:
        cursor.close()


def update_user(id: int, login: str, password: str, groupname: str) -> bool:
    file = 'update_user.sql'

    salt, hashed_password = hasher.hash_password(password)

    params = (login, hashed_password, salt, get_group_by_name(groupname).id, id)

    cursor = get_cursor()

    try:
        cursor.execute(read_sql_file(file), params)
    except Exception as e:
        print(e)
        return False
    else:
        return True


def delete_user_by_id(id: int) -> bool:
    file = 'delete_user_by_id.sql'

    cursor = get_cursor()

    try:
        cursor.execute(read_sql_file(file), (id,))

    except Exception as e:
        print(e)
        return False

    else:
        return True

    finally:
        cursor.close()


def delete_user_by_login(login: str) -> bool:
    file = 'delete_user_by_login.sql'

    cursor = get_cursor()

    try:
        cursor.execute(read_sql_file(file), (login,))

    except Exception as e:
        print(e)
        return False

    else:
        return True

    finally:
        cursor.close()
