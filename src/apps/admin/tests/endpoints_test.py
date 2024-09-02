import os
import pytest

from fastapi.testclient import TestClient

from src.apps.common.database.connection import close_connection, get_or_create_connection
from src.apps.admin.database.DAOs import groupDAO, userDAO
from src.apps.admin.database.models.rights import Rights 
from src.main import app

TEST_DB_FILE_NAME = 'test.db'

groups_data = [
    ('super-user', Rights.FULL),
    ('default-user', Rights.READ_WRITE),
    ('restricted-user', Rights.READ_ONLY),
]

users_data = [
    ('super-user', 'password'),
    ('default-user', 'password'),
    ('restricted-user', 'password'),
]


def clear_db():
    for user in userDAO.get_all_users():
        userDAO.delete_user_by_id(user.id)

    for group in groupDAO.get_all_groups():
        groupDAO.delete_group_by_id(group.id)


def create_db():
    for i in range(3):
        group = groups_data[i]
        user = users_data[i]

        created_group, created = groupDAO.create_group(group[0], group[1])

        if not created:
            pytest.fail("Can't create group: " + group[0])
        
        _, created = userDAO.create_user(user[0], user[1], created_group)

        if not created:
            pytest.fail("Can't create user: " + user[0])



@pytest.fixture(scope="session", autouse=True)
def setup():
    get_or_create_connection(TEST_DB_FILE_NAME)
    clear_db()
    create_db()

    yield

    close_connection()
    os.remove(TEST_DB_FILE_NAME)


client = TestClient(app)
token: str = ''
headers: dict = {}


def test_get_jwt():
    global token
    global headers

    form = {
        'username':'super-user',
        'password':'password'
    }

    headers = {
        'Content-Type':'application/x-www-form-urlencoded',
        'Content-Length': str(sum([len(i) for i in form.values()])),
        'Accept-Type':'application/json',
        'User-Agent':'Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion'
    }
    
    response = client.post(url='/login', 
                           data=form, 
                           headers=headers)    

    assert response.status_code == 200
    
    token = response.json().get('token', '')
    headers = {
        'Accept-Type':'application/json',
        'User-Agent':'Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion',
        'Authorization' : f'Bearer {token}'
    }
    
    assert token != ''


def test_get_all_groups():
    headers = {
        'Accept-Type':'application/json',
        'User-Agent':'Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion',
        'Authorization' : f'Bearer {token}'
    }

    response = client.get('/admin/groups', headers=headers)

    assert response.status_code == 200

    groups = sorted([data['name'] for data in response.json()])
    actual_groups = sorted([data[0] for data in groups_data])

    assert groups == actual_groups


def test_get_all_users():
    response = client.get('/admin/users', headers=headers)

    assert response.status_code == 200

    users = sorted([data['login'] for data in response.json()])
    actual_users = sorted([data[0] for data in users_data])

    assert users == actual_users


# Тестирование GET /admin/groups/{id}
@pytest.mark.dependency()
def test_get_group():
    response = client.get('/admin/groups/', headers=headers)

    group = response.json()[0]

    response = client.get(f"/admin/groups/{group['id']}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == group['id']


# Тестирование POST admin/groups
@pytest.mark.dependency()
def test_add_group():
    data = {
        "groupname": "new-group",
        "rights": "Read-Only",
    }

    response = client.post("/admin/groups/", headers=headers, data=data)

    assert response.status_code == 201
    assert response.json()["name"] == "new-group"

# Тестирование PUT /groups/{id}
@pytest.mark.dependency(depends=["test_add_group"])
def test_update_group():
    response = client.get('/admin/groups/', headers=headers)

    group = [data for data in response.json() if data['name']=='new-group'][0]

    data = {
        "groupname": "updated-group",
        "rights": "Read-Write"
    }
    response = client.put(f"/admin/groups/{group['id']}", headers=headers, data=data)
    assert response.status_code == 200
    assert response.json()["name"] == "updated-group"

# Тестирование DELETE admin/groups/{id_or_name}
@pytest.mark.dependency(depends=["test_add_group", "test_update_group"])
def test_delete_group_by_id_or_name():
    group_name = 'updated-group'  # Удаляем группу с id=1
    response = client.delete(f"/admin/groups/{group_name}", headers=headers)
    assert response.status_code == 200
    assert response.json() == "group deleted"

    group_name = "new-group"
    response = client.delete(f"/admin/groups/{group_name}", headers=headers)
    assert response.status_code == 200
    assert response.json() == "group deleted"


