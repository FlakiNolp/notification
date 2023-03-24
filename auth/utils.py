import sqlalchemy.exc
from sqlalchemy.orm import Session
from auth.models import User
from fastapi import HTTPException, status


def get_user_by_email(email: str, db: Session):
    try:
        return db.query(User).where(User.email == email).one()
    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )