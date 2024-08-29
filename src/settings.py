import os, pathlib
import dotenv

dotenv.load_dotenv(".env")

SRC_DIR: pathlib.Path = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))

PROJECT_DIR = os.path.join(SRC_DIR.parent)

FILES_DIR = os.path.join(PROJECT_DIR, 'files')

SQL_DIRS = [
    SRC_DIR / "apps/admin/database/DAOs/SQL",
    SRC_DIR / "apps/common/database/SQL",
]

DATABASE_CONNECTION_OPTIONS = {
    'NAME': os.environ.get("SQL_DATABASE_NAME", 'data.db'),
}

JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
JWT_ALGORITHM = "HS256"
JWT_TOKEN_EXPIRE_SECONDS = 3600
