import os
import pytest

from src.apps.admin.database.models.rights import Rights
from src.apps.common.database.connection import get_cursor, close_connection, get_or_create_connection
from src.apps.admin.database.DAOs import userDAO, groupDAO

TEST_DB_FILE_NAME = 'test.db'


def setup():
    get_or_create_connection(TEST_DB_FILE_NAME)


def teardown():
    close_connection()
    os.remove(TEST_DB_FILE_NAME)


def test_admin_create_and_get_user():
    group, created = groupDAO.create_group('test', rights=Rights.FULL)

    if not created:
        pytest.fail('Failed to create group')

    user, created = userDAO.create_user('test', 'test', group)

    if not created:
        pytest.fail('Failed to create user')

    assert user.login == 'test'
    assert user.group.name == 'test'
    assert user.group.rights == Rights.FULL
