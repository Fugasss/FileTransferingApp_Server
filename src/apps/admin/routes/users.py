from typing import Annotated

from fastapi import APIRouter, Form
from starlette import status

from starlette.responses import JSONResponse

from src.apps.admin.database.DAOs import userDAO

router = APIRouter(prefix="/users", tags=["users"])


@router.get('/{id}', status_code=status.HTTP_200_OK)
def get_user(id: int | str):
    if id.isdigit():
        user = userDAO.get_user_by_id(id)
    else:
        user = userDAO.get_user_by_login(id)

    if user is None:
        return JSONResponse({'message': 'User not found'}, status_code=404)
    else:
        return user


@router.get('/')
def get_all_users():
    return userDAO.get_all_users()


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_user(username: Annotated[str, Form()], password: Annotated[str, Form()], groupname: Annotated[str, Form()]):
    group = userDAO.get_group_by_name(groupname)

    if group is None:
        return JSONResponse({'message': 'Group not found'}, status_code=404)
    else:
        user, created = userDAO.create_user(username, password, group)
        if created:
            return user
        else:
            return JSONResponse({'message': 'User creation failed'}, status_code=404)


@router.put('/{id}', status_code=status.HTTP_200_OK)
def update_user(id: int, username: Annotated[str, Form()], password: Annotated[str, Form()],
                groupname: Annotated[str, Form()]):
    if userDAO.update_user(id, username, password, groupname):
        return userDAO.get_user_by_id(id)
    else:
        return JSONResponse({'message': 'User update failed'}, status_code=404)


@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete_user_by_id(id: int | str):
    delete_user = userDAO.delete_user_by_id if id.isdigit() else userDAO.delete_user_by_login

    if delete_user(id):
        return JSONResponse({'message': 'User successfully deleted'}, status_code=200)
    else:
        return JSONResponse({'message': 'User deletion failed'}, status_code=404)
