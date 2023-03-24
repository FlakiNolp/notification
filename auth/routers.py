from fastapi import Depends, HTTPException, status, APIRouter, Cookie
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt
from auth.database import get_db
from sqlalchemy.orm import Session
import auth.utils as users_utils
from auth.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_HOURS
import hashlib

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Authenticate user
def authenticate_user(email: str, password: str, db: Session):
    user = users_utils.get_user_by_email(email, db)
    if not user:
        return False
    if not hashlib.sha256(password.encode()).hexdigest() == user.hashed_password:
        return False
    return user


# Create access token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Create refresh token
def create_refresh_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Decode token
def decode_token(token: str = Depends(oauth2_scheme)):
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

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(hours=REFRESH_TOKEN_EXPIRE_HOURS)
    access_token = create_access_token(
        data={"id": user.id}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"id": user.id}, expires_delta=refresh_token_expires
    )
    return JSONResponse(content={"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"})


# Create refresh token endpoint
@router.post("/refresh")
async def refresh_token_fun(refresh_token: str = Cookie()):
    id = decode_refresh_token(refresh_token)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(hours=REFRESH_TOKEN_EXPIRE_HOURS)
    access_token = create_access_token(
        data={"id": id}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"id": id}, expires_delta=refresh_token_expires
    )
    return JSONResponse(content={"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"})

