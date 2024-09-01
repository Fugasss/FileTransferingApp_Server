import os
import pytest

from src.apps.admin.database.models.rights import Rights
from src.apps.common.database.connection import close_connection, get_or_create_connection
from src.apps.admin.database.DAOs import userDAO, groupDAO

TEST_DB_FILE_NAME = 'test.db'


@pytest.fixture(scope="module", autouse=True)
def setup():
    get_or_create_connection(TEST_DB_FILE_NAME)

    yield

    close_connection()
    os.remove(TEST_DB_FILE_NAME)


@pytest.mark.dependency()
def test_create_groups():
    groups = [
        ('group1', Rights.READ_ONLY),
        ('group2', Rights.READ_ONLY),
        ('group3', Rights.READ_WRITE),
        ('group4', Rights.READ_WRITE),
        ('group5', Rights.FULL),
        ('group6', Rights.FULL),
    ]

    for group_name, rights in groups:
        group, created = groupDAO.create_group(name=group_name, rights=rights)

        if not created:
            pytest.fail('Failed to create group')

        assert group.name == group_name
        assert group.rights == rights


@pytest.mark.dependency(depends=['test_create_groups'])
def test_create_and_get_users():
    users = [
        ('user1', 'pass1', 'group1'),
        ('user2', 'pass2', 'group2'),
        ('user3', 'pass3', 'group3'),
        ('user4', 'pass4', 'group4'),
        ('user5', 'pass5', 'group5'),
        ('user6', 'pass6', 'group6'),
    ]

    for user_name, user_password, group_name in users:
        group = groupDAO.get_group_by_name(group_name)

        if not group:
            pytest.fail('Failed to get group')

        user, created = userDAO.create_user(user_name, user_password, group)

        if not created:
            pytest.fail('Failed to create user')

        assert user.login == user_name
        assert user.group.name == group_name


@pytest.mark.dependency(depends=['test_create_and_get_users'])
def test_update_users():
    old_data = [
        'user1',
        'user2',
        'user3',
        'user4',
        'user5',
        'user6',
    ]

    new_data = [
        ('user1_1', 'pass1_1', 'group6'),
        ('user2_1', 'pass2_1', 'group5'),
        ('user3_1', 'pass3_1', 'group4'),
        ('user4_1', 'pass4_1', 'group3'),
        ('user5_1', 'pass5_1', 'group2'),
        ('user6_1', 'pass6_1', 'group1'),
    ]

    for it, data in enumerate(new_data):
        user = userDAO.get_user_by_login(old_data[it])

        if not user:
            pytest.fail('Failed to get user by login: {}'.format(old_data[it]))

        user_id = user.id

        updated = userDAO.update_user(user_id, data[0], data[1], data[2])

        if not updated:
            pytest.fail('Failed to update user')

        user = userDAO.get_user_by_id(user_id)

        if not user:
            pytest.fail('Failed to get updated user by id')

        assert user.id == user_id
        assert user.login == data[0]
        assert user.group.name == data[2]


@pytest.mark.dependency(depends=['test_create_and_get_users', 'test_update_users'])
def test_delete_users():
    users = [
        'user1_1',
        'user2_1',
        'user3_1',
        'user4_1',
        'user5_1',
        'user6_1'
    ]

    for user_name in users:
        deleted = userDAO.delete_user_by_login(user_name)

        if not deleted:
            pytest.fail('Failed to delete user')

        user = userDAO.get_user_by_login(user_name)

        assert user is None


@pytest.mark.dependency(depends=['test_create_groups', 'test_delete_users'])
def test_update_groups():
    old_data = [
        'group1',
        'group2',
        'group3',
        'group4',
        'group5',
        'group6',
    ]

    new_data = [
        ('group1_1', Rights.FULL),
        ('group2_1', Rights.FULL),
        ('group3_1', Rights.READ_WRITE),
        ('group4_1', Rights.READ_WRITE),
        ('group5_1', Rights.READ_ONLY),
        ('group6_1', Rights.READ_ONLY),
    ]

    for it, group_name in enumerate(old_data):
        group = groupDAO.get_group_by_name(group_name)

        if not group:
            pytest.fail('Failed to get group')

        group_id = group.id
        new = new_data[it]

        updated = groupDAO.update_group(group_id, new[0], new[1])

        if not updated:
            pytest.fail('Failed to update group')

        group = groupDAO.get_group_by_id(group_id)

        assert group.name == new[0]
        assert group.rights == new[1]


@pytest.mark.dependency(depends=['test_create_groups', 'test_update_groups'])
def test_delete_groups():
    groups = [
        'group1_1',
        'group2_1',
        'group3_1',
        'group4_1',
        'group5_1',
        'group6_1',
    ]

    for group_name in groups:
        deleted = groupDAO.delete_group_by_name(group_name)

        if not deleted:
            pytest.fail('Failed to delete group')

        group = groupDAO.get_group_by_name(group_name)

        assert group is None
