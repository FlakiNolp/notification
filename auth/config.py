from os import getenv

DB_USER = getenv("DB_USER", "postgres")
DB_PASSWORD = getenv("DB_PASSWORD", "postgres")
DB_HOST = getenv("DB_HOST", "localhost")
DB_PORT = getenv("DB_PORT", 6543)
SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
REFRESH_TOKEN_EXPIRE_HOURS = int(getenv("REFRESH_TOKEN_EXPIRE_HOURS", 24*30))