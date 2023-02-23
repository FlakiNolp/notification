from sqlalchemy.orm import Session
from app.models.users import User, Notification
from fastapi import HTTPException, status
import time
import random
from app.utils.utils import get_hash


def get_user_by_id(id: int, db: Session):
    return db.query(User).where(User.id == id).one()


def check_email(email: str, db: Session):
    try:
        db.query(User).where(email == User.email).one()
    except:
        return True
    raise HTTPException(
        status_code=status.HTTP_412_PRECONDITION_FAILED,
        detail="User already exist, try log-in",
    )
    #try:
    #    api_token = str(time.time() // 1)[:6] + ":" + get_hash((email + password) * random.randint(10, 101))
    #    user = insert(User).values(email=email, hashed_password=get_hash(password), api_token=api_token)
    #    db.execute(user)
    #    db.commit()
    #except Exception as e:
    #    raise HTTPException(
    #        status_code=status.HTTP_412_PRECONDITION_FAILED,
    #        detail="User already exist, try log-in",
    #    )


def new_user(email: str, hashed_password: str, db: Session):
    try:
        count = db.query(User).count() + 1
        api_token = str(int((time.time() % 1) * 1000000)) + ":" + get_hash((email + hashed_password) * random.randint(10, 101))
        user = User(id=count, email=email, hashed_password=hashed_password, api_token=api_token)
        services = Notification(user_id=count)
        db.add_all([user, services])
        db.commit()
    except:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail="User already exist, try log-in",
        )
