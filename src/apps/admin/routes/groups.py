from tokenize import group

from fastapi import HTTPException
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
        raise HTTPException(status_code=404, detail='Group not found')
    else:
        return group


@router.get('/', status_code=status.HTTP_200_OK)
def get_groups():
    return groupDAO.get_all_groups()


@router.post('/', status_code=status.HTTP_201_CREATED)
def add_group(groupname: Annotated[str, Form()],
              rights: Annotated[Rights, Form()],
              ):
    if rights in list(Rights):
        group, created = groupDAO.create_group(groupname, Rights(rights))

        if created:
            return group
        else:
            raise HTTPException(status_code=404, detail='Group creation failed')
    else:
        raise HTTPException(status_code=404, detail=f'No such rights: {rights}')


@router.put('/{id}', status_code=status.HTTP_200_OK)
def update_group(id: int,
                 groupname: Annotated[str, Form()],
                 rights: Annotated[Rights, Form()],
                 ):

    if groupDAO.get_group_by_id(id) is None:
        raise HTTPException(status_code=404, detail='Group not found')

    if groupDAO.update_group(id, groupname, Rights(rights)):
        return groupDAO.get_group_by_id(id)
    else:
        raise HTTPException(status_code=404, detail='Group update failed')


@router.delete('/{id_or_name}', status_code=status.HTTP_200_OK)
def delete_group_by_id_or_name(id_or_name: int | str):
    delete_group = groupDAO.delete_group_by_id if id_or_name.isdigit() else groupDAO.delete_group_by_name

    if delete_group(id_or_name):
        return JSONResponse('group deleted')
    else:
        raise HTTPException(status_code=404, detail='Group not found')
