from typing import Annotated

from fastapi import APIRouter, Form
from starlette import status

from starlette.responses import JSONResponse

from src.apps.admin.database.DAOs.groupDAO import get_group_by_id as get_group_by_id_dao
from src.apps.admin.database.DAOs.groupDAO import get_all_groups as get_all_groups_dao
from src.apps.admin.database.DAOs.groupDAO import create_group as create_group_dao
from src.apps.admin.database.DAOs.groupDAO import update_group as update_group_dao
from src.apps.admin.database.DAOs.groupDAO import delete_group_by_name as delete_group_by_name_dao
from src.apps.admin.database.DAOs.groupDAO import delete_group_by_id as delete_group_by_id_dao
from src.apps.admin.database.models.rights import Rights

router = APIRouter()


@router.get('/groups/{id}', status_code=status.HTTP_200_OK)
def get_group(id: int):
    group = get_group_by_id_dao(id)

    if group is None:
        return JSONResponse('Group not found', status_code=404)
    else:
        return group


@router.get('/groups', status_code=status.HTTP_200_OK)
def get_groups():
    return get_all_groups_dao()


@router.post('/groups', status_code=status.HTTP_201_CREATED)
def add_group(groupname: Annotated[str, Form()], rights: Annotated[Rights, Form()]):
    if rights in list(Rights):
        group, created = create_group_dao(groupname, Rights(rights))

        if created:
            return group
        else:
            return JSONResponse('Group creation failed', status_code=404)
    else:
        return JSONResponse('No such Rights', status_code=404)


@router.put('/groups/{id}', status_code=status.HTTP_200_OK)
def update_group(id: int, groupname: Annotated[str, Form()], rights: Annotated[Rights, Form()]):
    if update_group_dao(id, groupname, Rights(rights)):
        return get_group_by_id_dao(id)
    else:
        return JSONResponse('Update group failed', status_code=404)


@router.delete('/groups/id', status_code=status.HTTP_200_OK)
def delete_group_by_id(id: int):
    if delete_group_by_id_dao(id):
        return JSONResponse('group deleted')
    else:
        return JSONResponse('Group for deletion not found', status_code=404)


@router.delete('/groups/name', status_code=status.HTTP_200_OK)
def delete_group_by_id(name: str):
    if delete_group_by_name_dao(name):
        return JSONResponse('group deleted')
    else:
        return JSONResponse('Group for deletion not found', status_code=404)
