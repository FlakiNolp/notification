from fastapi import HTTPException, status
from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session
import auth.utils.db_utils as db_utils
from auth.config import SECRET_KEY, ALGORITHM
import hashlib


def authenticate_user(email: str, password: str, db: Session):
    user = db_utils.get_user_by_email(email, db)
    if not user:
        return False
    if not hashlib.sha256(password.encode()).hexdigest() == user.hashed_password:
        return False
    return user


def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str):
    try:
        payload = jwt.decode(token[7:], SECRET_KEY, algorithms=ALGORITHM)
        id: int = payload.get("id")
        if id is None:
            raise JWTError
        return id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def decode_refresh_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id: int = payload.get("id")
        if id is None:
            raise JWTError
        return id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )