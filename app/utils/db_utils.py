from sqlalchemy.orm import Session
from app.database.models import User, Notification
from fastapi import HTTPException, status
import time
from app.utils.utils import get_hash
import sqlalchemy.exc
import uuid


def get_services_by_id(id: int, db: Session):
    try:
        user = db.query(User).where(User.id == id).one()
        result = user.services.__dict__
        result.update({"api_token": user.api_token})
        return result
    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_email_by_id(id: int, db: Session):
    try:
        email = db.query(User).where(User.id == id).one().email
        return email
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def check_email(email: str, db: Session):
    try:
        db.query(User).where(email == User.email).one()
    except:
        return True
    raise HTTPException(
        status_code=status.HTTP_412_PRECONDITION_FAILED,
        detail="User already exist, try log-in",
    )


def new_user(email: str, hashed_password: str, db: Session):
    try:
        count = db.query(User).count() + 1
        api_token = str(int((time.time() % 1) * 10000000000000000)) + ":" + str(uuid.uuid4())
        user = User(id=count, email=email, hashed_password=hashed_password, api_token=api_token)
        services = Notification(user_id=count, email=email)
        db.add_all([user, services])
        db.commit()
    except:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail="User already exist, try log-in",
        )


def edit_services(db: Session, user_id: int, email: str = None, telegram_id: int = None, vk_domain: str = None,
                  website: str = None):
    try:
        services = db.query(Notification).where(Notification.user_id == user_id).one()
        services.email = email
        services.telegram_id = telegram_id
        services.vk_domain = vk_domain
        services.website = website
        db.commit()
    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )


def update_api_token(db: Session, user_id: int):
    try:
        services = db.query(User).where(User.id == user_id).one()
        api_token = str(int((time.time() % 1) * 10000000000000000)) + ":" + str(uuid.uuid4())
        services.api_token = api_token
        db.commit()
        return api_token
    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )


def reset_password(db: Session, user_id: int, password: str):
    try:
        user = db.query(User).where(User.id == user_id).one()
        user.hashed_password = get_hash(password)
        db.commit()
    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
