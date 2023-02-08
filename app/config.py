from os import getenv
from fastapi.templating import Jinja2Templates


secret_key = getenv("SECRET_KEY", "secret")
templates = Jinja2Templates(directory="templates")