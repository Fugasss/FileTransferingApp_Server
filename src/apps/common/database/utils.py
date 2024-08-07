import os.path
import typing

from .connection import get_cursor
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


def execute_and_fetchone(sql_file, vars: typing.Sequence | None = None):
    with get_cursor() as cursor:
        cursor.execute(read_sql_file(sql_file), vars)
        value = cursor.fetchone()

    return value


def execute_and_fetchall(sql_file, vars: typing.Sequence | None = None):
    with get_cursor() as cursor:
        cursor.execute(read_sql_file(sql_file), vars)
        value = cursor.fetchall()

    return value
