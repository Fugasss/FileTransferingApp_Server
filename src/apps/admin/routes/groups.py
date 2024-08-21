from typing import Annotated

from fastapi import APIRouter, Form
from starlette import status

from starlette.responses import JSONResponse

from src.apps.admin.database.DAOs import groupDAO
from src.apps.admin.database.models.rights import Rights

router = APIRouter(prefix="/groups", tags=["groups"])


@router.get('/{id}', status_code=status.HTTP_200_OK)
def get_group(id: int):
    group = groupDAO.get_group_by_id(id)

    if group is None:
        return JSONResponse('Group not found', status_code=404)
    else:
        return group


@router.get('/', status_code=status.HTTP_200_OK)
def get_groups():
    return groupDAO.get_all_groups()


@router.post('/', status_code=status.HTTP_201_CREATED)
def add_group(groupname: Annotated[str, Form()], rights: Annotated[Rights, Form()]):
    if rights in list(Rights):
        group, created = groupDAO.create_group(groupname, Rights(rights))

        if created:
            return group
        else:
            return JSONResponse('Group creation failed', status_code=404)
    else:
        return JSONResponse('No such Rights', status_code=404)


@router.put('/{id}', status_code=status.HTTP_200_OK)
def update_group(id: int, groupname: Annotated[str, Form()], rights: Annotated[Rights, Form()]):
    if groupDAO.update_group(id, groupname, Rights(rights)):
        return groupDAO.get_group_by_id(id)
    else:
        return JSONResponse('Update group failed', status_code=404)


@router.delete('/id', status_code=status.HTTP_200_OK)
def delete_group_by_id(id: int):
    if groupDAO.delete_group_by_id(id):
        return JSONResponse('group deleted')
    else:
        return JSONResponse('Group for deletion not found', status_code=404)


@router.delete('/name', status_code=status.HTTP_200_OK)
def delete_group_by_id(name: str):
    if groupDAO.delete_group_by_name(name):
        return JSONResponse('group deleted')
    else:
        return JSONResponse('Group for deletion not found', status_code=404)
