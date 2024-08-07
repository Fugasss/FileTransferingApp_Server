import typing

from .connection import get_cursor


def read_sql_file(sql_file):
    with open(sql_file, 'r', encoding='utf-8') as f:
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
