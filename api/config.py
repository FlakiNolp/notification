from os import getenv


email_password = getenv("EMAIL_PASSWORD")
telegram_api_key = getenv("TELEGRAM_API_KEY")
vk_api_key = getenv("VK_API_KEY")
logs_path = getenv("LOGS_PATH", r"C:\Users\maksi\PycharmProjects\team_project\logs")