from os import getenv
from fastapi.templating import Jinja2Templates


email_password = getenv("EMAIL_PASSWORD")
telegram_api_key = getenv("TELEGRAM_API_KEY")
vk_api_key = getenv("VK_API_KEY")
logs_path = getenv("LOGS_PATH", r"C:\Users\maksi\PycharmProjects\team_project\logs")
dp_path = getenv("DP_PATH", r"C:\Users\maksi\PycharmProjects\team_project\users.db")
secret_key = getenv("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
templates = Jinja2Templates(directory="templates")