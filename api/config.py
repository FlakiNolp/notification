from os import getenv

DB_USER = getenv("DB_USER", "postgres")
DB_PASSWORD = getenv("DB_PASSWORD", "postgres")
DB_HOST = getenv("DB_HOST", "localhost")
DB_PORT = getenv("DB_PORT", 6543)
EMAIL_PASSWORD = getenv("EMAIL_PASSWORD")
TELEGRAM_API_KEY = getenv("TELEGRAM_API_KEY")
VK_API_KEY = getenv("VK_API_KEY")
LOGS_PATH = getenv("LOGS_PATH", r"/usr/src/api/logs")
