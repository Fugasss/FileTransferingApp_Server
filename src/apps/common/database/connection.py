import sqlite3.dbapi2 as sqlite
import contextlib
from src import settings
from src.apps.common.database.utils import read_sql_file

__connection: sqlite.Connection | None = None


def __create_tables(cursor):
    cursor.executescript(read_sql_file('create_necessary_tables.sql'))
    cursor.executescript(read_sql_file('insert_necessary_data.sql'))


def get_or_create_connection():
    global __connection

    if __connection is None:
        options = settings.DATABASE_CONNECTION_OPTIONS
        name = options['NAME']

        __connection = sqlite.connect(database=name, isolation_level="IMMEDIATE", check_same_thread=False)
        __connection.close()

        __connection = sqlite.connect(database=name, isolation_level="IMMEDIATE", check_same_thread=False)

        with contextlib.closing(__connection.cursor()) as cursor:
            cursor.execute(read_sql_file('check_for_tables_existance.sql'))
            value = cursor.fetchone()
            
            if value[0] == 0:
                __create_tables(cursor)

    return __connection


def close_connection():
    global __connection
    __connection.commit()
    __connection.close()


def get_cursor():
    conn = get_or_create_connection()
    if conn is None:
        return
    return conn.cursor()
