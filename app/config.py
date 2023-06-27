from os import getenv
from fastapi.templating import Jinja2Templates

DB_USER = getenv("DB_USER", "postgres")
DB_PASSWORD = getenv("DB_PASSWORD", "postgres")
DB_HOST = getenv("DB_HOST", "localhost")
DB_PORT = getenv("DB_PORT", 6543)
HOST_DOMAIN = getenv("HOST_DOMAIN", "localhost")
SECRET_KEY = getenv("SECRET_KEY")
EMAIL_PASSWORD = getenv("EMAIL_PASSWORD")
templates = Jinja2Templates(directory="templates")