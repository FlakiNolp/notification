from fastapi import Depends, HTTPException, status, APIRouter, Cookie
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from auth.database.connection import get_db
from sqlalchemy.orm import Session
from auth.config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_HOURS
import auth.utils.auth as auth_utils

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth_utils.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(hours=REFRESH_TOKEN_EXPIRE_HOURS)
    access_token = auth_utils.create_token(
        data={"id": user.id}, expires_delta=access_token_expires
    )
    refresh_token = auth_utils.create_token(
        data={"id": user.id}, expires_delta=refresh_token_expires
    )
    return JSONResponse(content={"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"})


# Create refresh token endpoint
@router.post("/refresh")
async def refresh_token_fun(refresh_token: str = Cookie()):
    id = auth_utils.decode_refresh_token(refresh_token)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(hours=REFRESH_TOKEN_EXPIRE_HOURS)
    access_token = auth_utils.create_token(
        data={"id": id}, expires_delta=access_token_expires
    )
    refresh_token = auth_utils.create_token(
        data={"id": id}, expires_delta=refresh_token_expires
    )
    return JSONResponse(content={"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"})