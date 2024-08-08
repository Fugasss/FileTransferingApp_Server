import os, pathlib

BASE_DIR: pathlib.Path = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))

SQL_DIRS = [
    BASE_DIR / "apps/admin/database/DAOs/SQL",
    BASE_DIR / "apps/common/database/SQL",
]

DATABASE_CONNECTION_OPTIONS = {
    'NAME': os.environ.get("SQL_DATABASE_NAME", 'FileTransferingApp'),
    'HOST': os.environ.get("SQL_HOST", 'localhost'),
    'PORT': os.environ.get("SQL_PORT", '5432'),
    'USER': os.environ.get("SQL_USER", 'postgres'),
    'PASSWORD': os.environ.get("SQL_PASSWORD", 'postgres'),
}
