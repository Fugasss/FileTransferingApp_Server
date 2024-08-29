import os.path
import typing

from src.settings import SQL_DIRS


def find_file_in_dirs(dirs: typing.Sequence[str], file: typing.AnyStr) -> typing.AnyStr | None:
    for dir in dirs:
        for root, folders, files in os.walk(dir):
            if file in files:
                return os.path.join(root, file)

    return None


def read_sql_file(sql_file):
    path = find_file_in_dirs(SQL_DIRS, sql_file)

    if path is None:
        msg = f'{sql_file} not found in following directories: {SQL_DIRS}'
        raise FileNotFoundError(msg)

    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def list_of_all_files(path: str) -> list[str]:
    try:
        all_items = os.listdir(path)
        files = [item for item in all_items if os.path.isfile(os.path.join(path, item))]

        if ".gitkeep" in files:
            files.remove(".gitkeep")

        return files

    except Exception as e:
        raise e


def is_in_files(filename: str, path: str) -> bool:
    return filename in list_of_all_files(path)


def delete_file(filename: str, path: str) -> bool:
    if is_in_files(filename, path):
        os.remove(os.path.join(path, filename))
        return True
    else:
        return False