from fastapi import HTTPException, status
from jose import JWTError, jwt
from app.config import secret_key


def decode_token(token: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms="HS256")
        username: str = payload.get("sub")
        if username is None:
            raise JWTError
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )