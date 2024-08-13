from typing import Annotated

from fastapi import APIRouter, Form
from starlette import status

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


@router.get('/users/{id}', status_code=status.HTTP_200_OK)
def get_user(id: int):
    user = get_user_by_id_dao(id)

    if user is None:
        return JSONResponse('User not found', status_code=404)
    else:
        return user


@router.get('/users')
def get_all_users():
    return get_all_users_dao()


@router.post('/users', status_code=status.HTTP_201_CREATED)
def create_user(username: Annotated[str, Form()], password: Annotated[str, Form()], groupname: Annotated[str, Form()]):
    group = get_group_by_name_dao(groupname)

    if group is None:
        return JSONResponse('Group not found', status_code=404)
    else:
        user, created = create_user_dao(username, password, group)
        if created:
            return user
        else:
            return JSONResponse('User creation failed', status_code=404)


@router.put('/users/{id}', status_code=status.HTTP_200_OK)
def update_user(id: int, username: Annotated[str, Form()], password: Annotated[str, Form()], groupname: Annotated[str, Form()]):
    if update_user_dao(id, username, password, groupname):
        return dumps(get_user_by_id_dao(id))
    else:
        return JSONResponse('User update failed', status_code=404)


@router.delete('/users/id', status_code=status.HTTP_200_OK)
def delete_user_by_id(id: int):
    if delete_user_by_id_dao(id):
        return JSONResponse({'status': 'ok'}, status_code=200)
    else:
        return JSONResponse('User deletion failed', status_code=404)


@router.delete('/users/name', status_code=status.HTTP_200_OK)
def delete_user_by_login(login: str):
    if delete_user_by_login_dao(login):
        return JSONResponse({'status': 'ok'}, status_code=200)
    else:
        return JSONResponse('User deletion failed', status_code=404)
