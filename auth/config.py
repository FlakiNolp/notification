from os import getenv

secret_key = getenv("SECRET_KEY")
algorithm = getenv("ALGORITHM", "HS256")
access_token_expire_minutes = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
refresh_token_expire_hours = int(getenv("REFRESH_TOKEN_EXPIRE_HOURS", 24*30))