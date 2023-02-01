from os import getenv
from fastapi.templating import Jinja2Templates


email_password = getenv("EMAIL_PASSWORD")
telegram_api_key = getenv("TELEGRAM_API_KEY")
vk_api_key = getenv("VK_API_KEY")
logs_path = getenv("LOGS_PATH", r"C:\Users\maksi\PycharmProjects\team_project\logs")
dp_path = getenv("DP_PATH", r"C:\Users\maksi\PycharmProjects\team_project\users.db")
secret_key = getenv("SECRET_KEY", "789d43c1ea12dba05f31dc9dbfab688ee05de61c69a553d36752bfa28e9551ce")
templates = Jinja2Templates(directory="templates")