from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import List
from app.models.database import get_db
from sqlalchemy.orm import Session
import aunthefication_server.utils as users_utils
from passlib.context import CryptContext
from aunthefication_server.config import secret_key, algorithm, access_token_expire_minutes, refresh_token_expire_hours

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    refresh_token: str
    type: str


class TokenData(BaseModel):
    id: int
    role: List[str]


class User(BaseModel):
    username: str
    email: str
    hashed_password: str


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


# Authenticate user
def authenticate_user(email: str, password: str, db: Session):
    user = users_utils.get_user_by_email(email, db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# Create access token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


# Create refresh token
def create_refresh_token(data: dict, expires_delta: timedelta, access_token: str = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm, access_token=access_token)
    return encoded_jwt


# Decode token
def decode_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
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


def decode_refresh_token(token: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
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


# Create token endpoint
@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=access_token_expire_minutes)
    refresh_token_expires = timedelta(hours=refresh_token_expire_hours)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": user.email}, expires_delta=refresh_token_expires, access_token=access_token
    )
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


# Create refresh token endpoint
@router.post("/refresh")
async def refresh_token_fun(refresh_token: str):
    username = decode_refresh_token(refresh_token)
    access_token_expires = timedelta(minutes=access_token_expire_minutes)
    refresh_token_expires = timedelta(hours=refresh_token_expire_hours)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": username}, expires_delta=refresh_token_expires
    )
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}