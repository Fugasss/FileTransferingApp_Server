import os

from fastapi.testclient import TestClient

from src.apps.admin.database.DAOs import userDAO, groupDAO
from src.apps.common.database.connection import get_or_create_connection, close_connection

TEST_DB_FILE_NAME = 'test.db'


def create_test_db():
    try:
        os.remove(TEST_DB_FILE_NAME)
    except OSError:
        pass

    get_or_create_connection(TEST_DB_FILE_NAME)


def destroy_test_db():
    close_connection()
    os.remove(TEST_DB_FILE_NAME)


def clear_db():
    for user in userDAO.get_all_users():
        userDAO.delete_user_by_id(user.id)

    for group in groupDAO.get_all_groups():
        groupDAO.delete_group_by_id(group.id)


def add_admin_user_to_db():
    group, created = groupDAO.create_group('admin', 'Full')

    if not created:
        raise Exception('Failed to create group')

    user, created = userDAO.create_user('admin', 'password', group)

    if not created:
        raise Exception('Failed to create user')

    return user



def get_headers_with_auth(test_client: TestClient, user_info: dict[str, str] | None = None) -> dict[str, str]:

    if user_info is None:
        user_info = {
            'username': 'super-user',
            'password': 'password'
        }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': str(sum([len(i) for i in user_info.values()])),
        'Accept-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion'
    }

    response = test_client.post(url='/login',
                                data=user_info,
                                headers=headers)

    token = response.json().get('token', '')

    return {
        'Accept-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion',
        'Authorization': f'Bearer {token}'
    }
