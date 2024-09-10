import argparse

from src.apps.admin.database.DAOs import userDAO, groupDAO
from src.apps.admin.database.models.rights import Rights


def create_parser():
    parser = argparse.ArgumentParser(description="Command-line Admin App")
    parser.add_argument("-a", "--add", nargs=3, metavar="", help="Add a new user: -a [login] [password] [group name]")
    parser.add_argument("-ul", "--ulist", action="store_true", help="List all users")
    parser.add_argument("-r", "--remove", metavar="", help="Remove user by id: -r [id]")
    parser.add_argument("-c", "--change", nargs=2, metavar="", help="Change user group: -ch [id] [group name]")
    parser.add_argument("-g", "--group", nargs=2, metavar="", help="Add a new group: -g [name] [Rights: 1 - Full, 2 - Read-Only, 3 - Read-Write]")
    parser.add_argument("-gl", "--glist", action="store_true", help="List all groups")
    return parser


def add_user(login: str, password: str, groupname: str):
    group = groupDAO.get_group_by_name(groupname)

    if group is None:
        print('Group not found')
    else:
        user, created = userDAO.create_user(login, password, group)

        if created:
            print('User created successfully')
        else:
            print(f'User {login} already exists')


def list_users():
    users = userDAO.get_all_users()
    for user in users:
        print(f'id:{user.id}, login:{user.login}, {user.group}')


def remove_user(id: int):
    user = userDAO.get_user_by_id(id)

    if user is None:
        print('User not found')
    else:
        deleted = userDAO.delete_user_by_id(id)

        if deleted:
            print('User deleted successfully')
        else:
            print('User deletion error')


def change_user_group(id: int, groupname: str):
    group = groupDAO.get_group_by_name(groupname)

    if group is None:
        print('Group not found')
    else:
        user = userDAO.get_user_by_id(id)

        if user is None:
            print('User not found')
        else:
            changed = userDAO.update_user_group(id, groupname)

            if changed:
                print('User\'s group changed successfully')
            else:
                print('User\'s group changes error')

def add_group(groupname: str, rights: str):
    group = groupDAO.get_group_by_name(groupname)
    num_rights = ["1", "2", "3"]

    dict_rights = {"1": "Full", "2": "Read-Only", "3": "Read-Write"}

    if group is not None:
        print('Group with this name already exists')

    elif rights not in num_rights:
        print('Rights not found')

    else:
        group, created = groupDAO.create_group(groupname, Rights(dict_rights[rights]))

        if group is None or not created:
            print('Group creation error')
        else:
            print('Group created successfully')

def list_groups():
    groups = groupDAO.get_all_groups()
    for group in groups:
        print(f'id:{group.id}, groupname:{group.name}, rights:{group.rights}')

def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.add:
        add_user(*args.add)
    elif args.ulist:
        list_users()
    elif args.remove:
        remove_user(int(args.remove))
    elif args.change:
        change_user_group(int(args.change[0]), args.change[1])
    elif args.group:
        add_group(*args.group)
    elif args.glist:
        list_groups()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
