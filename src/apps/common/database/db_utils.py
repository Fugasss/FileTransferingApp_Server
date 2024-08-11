import contextlib
import typing

from src.apps.common.database.connection import get_cursor
from src.apps.common.database.utils import read_sql_file


def execute_and_fetchone(sql_file, vars: typing.Sequence | None = None):
    with contextlib.closing(get_cursor()) as cursor:
        cursor.execute(read_sql_file(sql_file), vars)
        value = cursor.fetchone()

    return value


def execute_and_fetchall(sql_file, vars: typing.Sequence | None = None):
    with contextlib.closing(get_cursor()) as cursor:
        cursor.execute(read_sql_file(sql_file), vars)
        value = cursor.fetchall()

    return value
