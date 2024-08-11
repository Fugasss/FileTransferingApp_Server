from fastapi import APIRouter

from starlette.responses import JSONResponse
from fastapi import HTTPException

from json import dumps

from src.apps.admin.database.DAOs.userDAO import get_all_users as get_all_users_dao
from src.apps.admin.database.DAOs.userDAO import get_user_by_id as get_user_by_id_dao
from src.apps.admin.database.DAOs.userDAO import create_user as create_user_dao
from src.apps.admin.database.DAOs.userDAO import update_user as update_user_dao
from src.apps.admin.database.DAOs.userDAO import delete_user_by_id as delete_user_by_id_dao
from src.apps.admin.database.DAOs.userDAO import delete_user_by_login as delete_user_by_login_dao
from src.apps.admin.database.DAOs.groupDAO import get_group_by_name as get_group_by_name_dao


router = APIRouter()


@router.get('/users/{id}')
def get_user(id: int):
    user = get_user_by_id_dao(id)

    if user is None:
        return HTTPException(status_code=404, detail='User not found')
    else:
        return dumps(user)


@router.get('/users')
def get_all_users():
    return dumps(get_all_users_dao())


@router.post('/users')
def create_user(username: str, password: str, groupname: str):
    group = get_group_by_name_dao(groupname)

    if group is None:
        return HTTPException(status_code=404, detail='Group not found')
    else:
        user, created = create_user_dao(username, password, group)
        if created:
            return dumps(user)
        else:
            return HTTPException(status_code=404, detail='User creation failed')


@router.put('/users/{id}')
def update_user(id: int, username: str, password: str, groupname: str):

    if update_user_dao(id, username, password, groupname):
        return dumps(get_user_by_id_dao(id))
    else:
        return HTTPException(status_code=404, detail='User not found')


@router.delete('/users/id')
def delete_user_by_id(id: int):
    if delete_user_by_id_dao(id):
        return JSONResponse({'status': 'ok'})
    else:
        return HTTPException(status_code=404, detail='User deletion failed')


@router.delete('/users/login')
def delete_user_by_login(login: str):
    if delete_user_by_login_dao(login):
        return JSONResponse({'status': 'ok'})
    else:
        return HTTPException(status_code=404, detail='User deletion failed')
