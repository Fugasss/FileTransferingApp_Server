import os

import dotenv
import psycopg as pg
from psycopg import cursor

from src import settings

__connection: pg.connection.Connection | None = None


def __database_exists(cursor, name: str) -> bool:
    cursor.execute(f'''
            SELECT exists(
                SELECT datname FROM pg_catalog.pg_database WHERE datname = %s
            );
    ''', (name,))

    return cursor.fetchone()[0]


def __create_database(cursor, name: str):
    cursor.execute('''
                CREATE DATABASE "{}" WITH
                OWNER = postgres
                ENCODING = 'UTF8'
            '''.format(name))


def __create_tables(cursor):
    from src.apps.common.database.utils import read_sql_file
    cursor.execute(read_sql_file('create_necessary_tables.sql'))
    cursor.execute(read_sql_file('insert_necessary_data.sql'))


def get_or_create_connection():
    global __connection

    options = settings.DATABASE_CONNECTION_OPTIONS
    host = options['HOST']
    name = options['NAME']
    port = options['PORT']
    user = options['USER']
    password = options['PASSWORD']

    if __connection is None:
        conn: pg.connection.Connection = pg.connect(host=host, port=port, user=user, password=password)
        conn.autocommit = True
        conn.set_isolation_level(pg.connection.IsolationLevel.READ_UNCOMMITTED)

        cursor = conn.cursor()

        if not __database_exists(cursor, name):
            __create_database(cursor, name)

        cursor.close()
        conn.close()

        __connection = pg.connect(dbname=name, host=host, port=port, user=user, password=password)
        __connection.autocommit = True

        with __connection.cursor() as cursor:
            __create_tables(cursor)

    return __connection


def get_cursor():
    conn = get_or_create_connection()
    if conn is None:
        return
    return conn.cursor()
