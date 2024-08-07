import os

import dotenv
import psycopg2 as pg
from psycopg2._psycopg import cursor
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

__connection: pg._psycopg.connection | None = None


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


def get_or_create_connection():
    global __connection

    name = os.environ.get("SQL_DATABASE_NAME", 'FileTransferingApp')
    host = os.environ.get("SQL_HOST", 'localhost')
    port = os.environ.get("SQL_PORT", '5432')
    user = os.environ.get("SQL_USER", 'postgres')
    password = os.environ.get("SQL_PASSWORD", 'postgres')

    if __connection is None:
        conn = pg.connect(host=host, port=port, user=user, password=password)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        conn.autocommit = True

        cursor = conn.cursor()

        if not __database_exists(cursor, name):
            __create_database(cursor, name)

        cursor.close()
        conn.close()

        __connection = pg.connect(database=name, host=host, port=port, user=user, password=password)
        __connection.autocommit = True

        with __connection.cursor() as cursor:
            __create_tables(cursor)

    return __connection


def get_cursor():
    conn = get_or_create_connection()
    if conn is None:
        return
    return conn.cursor()
