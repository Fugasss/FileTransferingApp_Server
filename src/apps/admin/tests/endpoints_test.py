import pytest

from fastapi.testclient import TestClient
from pytest_dependency import depends

from src.apps.admin.database.DAOs import groupDAO, userDAO
from src.apps.admin.database.models.rights import Rights
from src.main import app
from .test_utils import create_test_db, destroy_test_db, clear_db

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
    create_test_db()
    clear_db()
    create_db()
    yield
    destroy_test_db()


client = TestClient(app)
headers: dict = {}


@pytest.mark.dependency()
def test_get_jwt():
    global headers

    form = {
        'username': 'super-user',
        'password': 'password'
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': str(sum([len(i) for i in form.values()])),
        'Accept-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion'
    }

    response = client.post(url='/login',
                           data=form,
                           headers=headers)

    assert response.status_code == 200

    token = response.json().get('token', '')
    headers = {
        'Accept-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion',
        'Authorization': f'Bearer {token}'
    }

    assert token != ''


@pytest.mark.dependency(depends=["test_get_jwt"])
def test_get_all_groups():
    response = client.get('/admin/groups', headers=headers)

    assert response.status_code == 200

    groups = sorted([data['name'] for data in response.json()])
    actual_groups = sorted([data[0] for data in groups_data])

    assert groups == actual_groups


@pytest.mark.dependency(depends=["test_get_jwt"])
def test_get_group():
    response = client.get('/admin/groups/', headers=headers)

    group = response.json()[0]

    response = client.get(f"/admin/groups/{group['id']}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == group['id']


@pytest.mark.dependency(depends=["test_get_jwt"])
def test_add_group():
    data = {
        "groupname": "new-group",
        "rights": "Read-Only",
    }

    response = client.post("/admin/groups/", headers=headers, data=data)

    assert response.status_code == 201
    assert response.json()["name"] == "new-group"


@pytest.mark.dependency(depends=["test_add_group", "test_get_jwt"])
def test_update_group():
    response = client.get('/admin/groups/', headers=headers)

    group = [data for data in response.json() if data['name'] == 'new-group'][0]

    data = {
        "groupname": "updated-group",
        "rights": "Read-Write"
    }
    response = client.put(f"/admin/groups/{group['id']}", headers=headers, data=data)
    assert response.status_code == 200
    assert response.json()["name"] == "updated-group"



@pytest.mark.dependency(depends=["test_add_group", "test_get_jwt"])
def test_update_group_not_found():
    data = {
        "groupname": "non-updated-group",
        "rights": "Read-Write"
    }
    response = client.put(f"/admin/groups/999", headers=headers, data=data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Group not found"}


@pytest.mark.dependency(depends=["test_update_group", "test_get_jwt"])
def test_update_group_failed_due_to_non_existing_rights():
    response = client.get('/admin/groups/', headers=headers)
    group = [data for data in response.json() if data['name'] == 'updated-group'][0]

    data = {
        "groupname": "non-updated-group",
        "rights": "Read-Read"
    }
    response = client.put(f"/admin/groups/{group['id']}", headers=headers, data=data)

    # 422 error, because rights are annotated as Annotated[Rights, Form()],
    # so it automatically validates input of rights parameter
    assert response.status_code == 422


@pytest.mark.dependency(depends=["test_add_group", "test_update_group", "test_get_jwt"])
def test_delete_group_by_id_or_name():
    group_name = 'updated-group'  # Удаляем группу с id=1
    response = client.delete(f"/admin/groups/{group_name}", headers=headers)
    assert response.status_code == 200
    assert response.json() == "group deleted"

    group_name = "new-group"
    response = client.delete(f"/admin/groups/{group_name}", headers=headers)
    assert response.status_code == 200
    assert response.json() == "group deleted"


@pytest.mark.dependency(depends=["test_get_jwt"])
def test_get_all_users():
    response = client.get("/admin/users/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    users = sorted([data['login'] for data in response.json()])
    actual_users = sorted([data[0] for data in users_data])

    assert users == actual_users


@pytest.mark.dependency(depends=["test_get_all_users", "test_get_jwt"])
def test_get_user_by_id():
    response = client.get("/admin/users/1", headers=headers)
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["login"] == "super-user"


@pytest.mark.dependency(depends=["test_get_all_users", "test_get_jwt"])
def test_get_user_by_login():
    response = client.get("/admin/users/super-user", headers=headers)
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["login"] == "super-user"


@pytest.mark.dependency(depends=["test_get_all_users", "test_get_jwt"])
def test_get_user_not_found():
    response = client.get("/admin/users/999", headers=headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


@pytest.mark.dependency(depends=["test_get_jwt"])
def test_create_user():
    response = client.post(
        "/admin/users/",
        data={"username": "new-user", "password": "newpassword", "groupname": "default-user"},
        headers=headers,
    )
    assert response.status_code == 201
    user_data = response.json()
    assert user_data["login"] == "new-user"


@pytest.mark.dependency(depends=["test_create_user", "test_get_jwt"])
def test_create_user_failed_due_to_group_not_found():
    response = client.post(
        "/admin/users/",
        data={"username": "new-user2", "password": "newpassword", "groupname": "nonexistent-group"},
        headers=headers,
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Group not found"}


@pytest.mark.dependency(depends=["test_get_all_users", "test_create_user", "test_get_jwt"])
def test_update_user():
    response = client.get(f'/admin/users/new-user', headers=headers)
    user_data = response.json()
    print(user_data)
    response = client.put(
        f"/admin/users/{user_data['id']}",
        data={"username": "new-restricted-user", "password": "newpassword", "groupname": "restricted-user"},
        headers=headers,
    )
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["login"] == "new-restricted-user"


@pytest.mark.dependency(depends=["test_create_user", "test_get_jwt"])
def test_update_user_not_found():
    response = client.put(
        "/admin/users/999",
        data={"username": "non-existent-user", "password": "password", "groupname": "default-user"},
        headers=headers,
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "User update failed"}


@pytest.mark.dependency(depends=["test_create_user", "test_get_jwt"])
def test_delete_user_by_id():
    response = client.delete("/admin/users/4", headers=headers)
    assert response.status_code == 200


@pytest.mark.dependency(depends=["test_create_user", "test_get_jwt"])
def test_delete_user_by_login():
    response = client.delete("/admin/users/default-user", headers=headers)
    assert response.status_code == 200


@pytest.mark.dependency(depends=["test_delete_user_by_id", "test_get_jwt"])
def test_delete_user_failed_because_user_not_found():
    response = client.delete("/admin/users/999", headers=headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


