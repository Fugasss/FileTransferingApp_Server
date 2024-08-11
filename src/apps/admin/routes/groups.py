from fastapi import APIRouter

from starlette.responses import JSONResponse
from fastapi import HTTPException

from json import dumps

from src.apps.admin.database.DAOs.groupDAO import get_group_by_name as get_group_by_name_dao
from src.apps.admin.database.DAOs.groupDAO import get_group_by_id as get_group_by_id_dao
from src.apps.admin.database.DAOs.groupDAO import get_all_groups as get_all_groups_dao
from src.apps.admin.database.DAOs.groupDAO import create_group as create_group_dao
from src.apps.admin.database.DAOs.groupDAO import update_group as update_group_dao
from src.apps.admin.database.DAOs.groupDAO import delete_group_by_name as delete_group_by_name_dao
from src.apps.admin.database.DAOs.groupDAO import delete_group_by_id as delete_group_by_id_dao
from src.apps.admin.database.models.rights import Rights

router = APIRouter()

@router.get('/groups/{id}')
def get_group(id: int):
    group = get_group_by_id_dao(id)

    if group is None:
        return HTTPException(status_code=404, detail='Group not found')
    else:
        return dumps(group)


@router.get('/groups')
def get_groups():
    return dumps(get_all_groups_dao())


@router.post('/groups')
def add_group(groupname: str, rights: str):
    if rights in Rights:
        group, created = create_group_dao(groupname, Rights(rights))
        if created:
            return dumps(group)
        else:
            return HTTPException(status_code=404, detail='Group creation failed')
    else:
        return HTTPException(status_code=403, detail='No such Rights')


@router.put('/groups/{id}')
def update_group(id: int, groupname: str, rights: str):
    if update_group_dao(id, groupname, Rights(rights)):
        return dumps(get_group_by_id_dao(id))
    else:
        return HTTPException(status_code=404, detail='Update group failed')


@router.delete('/groups/id')
def delete_group_by_id(id: int):
    if delete_group_by_id_dao(id):
        return JSONResponse({'status': 'ok'})
    else:
        return HTTPException(status_code=404, detail='Group deletion failed')


@router.delete('/groups/name')
def delete_group_by_id(name: str):
    if delete_group_by_name_dao(name):
        return JSONResponse({'status': 'ok'})
    else:
        return HTTPException(status_code=404, detail='Group deletion failed')
