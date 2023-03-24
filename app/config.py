from os import getenv
from fastapi.templating import Jinja2Templates


HOST_DOMAIN = getenv("HOST_DOMAIN", "localhost")
SECRET_KEY = getenv("SECRET_KEY")
EMAIL_PASSWORD = getenv("EMAIL_PASSWORD")
templates = Jinja2Templates(directory="templates")