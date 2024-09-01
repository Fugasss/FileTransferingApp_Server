from typing import Annotated

from fastapi import APIRouter, Form, HTTPException
from starlette import status

from starlette.responses import Response

from src.apps.admin.database.DAOs import userDAO

router = APIRouter(prefix="/users", tags=["users"])


@router.get('/{id}', status_code=status.HTTP_200_OK)
def get_user(id: int | str):
    if id.isdigit():
        user = userDAO.get_user_by_id(id)
    else:
        user = userDAO.get_user_by_login(id)

    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail='User not found')


@router.get('/')
def get_all_users():
    return userDAO.get_all_users()


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_user(username: Annotated[str, Form()],
                password: Annotated[str, Form()],
                groupname: Annotated[str, Form()],
                ):
    group = userDAO.get_group_by_name(groupname)

    if group is None:
        raise HTTPException(status_code=404, detail='Group not found')

    user, created = userDAO.create_user(username, password, group)

    if created:
        return user
    else:
        raise HTTPException(status_code=404, detail='User creation failed')


@router.put('/{id}', status_code=status.HTTP_200_OK)
def update_user(id: int,
                username: Annotated[str, Form()],
                password: Annotated[str, Form()],
                groupname: Annotated[str, Form()],
                ):
    if userDAO.update_user(id, username, password, groupname):
        return userDAO.get_user_by_id(id)
    else:
        raise HTTPException(status_code=404, detail='User update failed')


@router.delete('/{id_or_name}', status_code=status.HTTP_200_OK)
def delete_user_by_id_or_name(id_or_name: int | str):
    delete_user = userDAO.delete_user_by_id if id_or_name.isdigit() else userDAO.delete_user_by_login

    if delete_user(id_or_name):
        return Response(status_code=200)
    else:
        raise HTTPException(status_code=404, detail='User not found')
