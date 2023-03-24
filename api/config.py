from os import getenv


EMAIL_PASSWORD = getenv("EMAIL_PASSWORD")
TELEGRAM_API_KEY = getenv("TELEGRAM_API_KEY")
VK_API_KEY = getenv("VK_API_KEY")
LOGS_PATH = getenv("LOGS_PATH", r"/usr/src/api/logs")