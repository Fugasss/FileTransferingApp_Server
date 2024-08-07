from src.apps.admin.database.DAOs.groupDAO import get_group_by_id
from src.apps.admin.database.models.user import User
from src.apps.admin.database.models.rights import Rights
from src.apps.admin.database.models.group import Group
from src.apps.admin.security import hasher
from src.apps.common.database.connection import get_cursor
from src.apps.common.database.utils import execute_and_fetchall, read_sql_file


def get_all_users() -> tuple[User]:
    users: list[User] = []
    data = execute_and_fetchall('./SQL/select_all_users.sql')

    for row in data:
        group = get_group_by_id(row[3])
        user = User(id=row[0], login=row[1], password=row[2], group=group)
        users.append(user)

    return tuple(*users)


def get_users_by_rights(rights: Rights) -> tuple[User]:
    raise NotImplementedError


def get_user_by_login(login) -> User | None:
    raise NotImplementedError


def create_user(login: str, password: str, group: Group) -> (User | None, bool):
    cursor = get_cursor()

    try:
        salt, hashed_password = hasher.hash_password(password)
        cursor.execute(read_sql_file('./SQL/create_user.sql'), (login, hashed_password, salt, group.id))

    except Exception as e:
        print(e)
        return None, False

    else:
        return get_user_by_login(login), True

    finally:
        cursor.close()


def update_user(user: User) -> bool:
    raise NotImplementedError


def delete_user(user: User) -> bool:
    raise NotImplementedError
