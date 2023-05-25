from fastapi import HTTPException, status
from jose import JWTError, jwt
from app.config import SECRET_KEY
from datetime import datetime, timedelta


def create_token(data: dict, expires_delta: int):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms="HS256")
        id: int = payload.get(f"id")
        if id is None:
            raise JWTError
        return id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def decode_registration_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms="HS256")
        email: str = payload.get(f"email")
        hashed_password = payload.get(f"hashed_password")
        if email is None or hashed_password is None:
            raise JWTError
        return email, hashed_password
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
