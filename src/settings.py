import os, pathlib
import dotenv

dotenv.load_dotenv(".env")

BASE_DIR: pathlib.Path = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))

SQL_DIRS = [
    BASE_DIR / "apps/admin/database/DAOs/SQL",
    BASE_DIR / "apps/common/database/SQL",
]

DATABASE_CONNECTION_OPTIONS = {
    'NAME': os.environ.get("SQL_DATABASE_NAME", 'data.db'),
}

JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
JWT_ALGORITHM = "HS256"
JWT_TOKEN_EXPIRE = 3600
