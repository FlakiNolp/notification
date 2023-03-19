from os import getenv
from fastapi.templating import Jinja2Templates
import os


secret_key = getenv("SECRET_KEY")
email_password = getenv("EMAIL_PASSWORD")
templates = Jinja2Templates(directory="templates")