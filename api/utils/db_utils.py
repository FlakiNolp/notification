import sqlalchemy.exc
from api.database.models import User, Notification
from sqlalchemy.orm import Session
from fastapi import status, HTTPException


def get_user_email_by_api_token(api_token: str, db: Session):
    try:
        return db.query(User).where(api_token == User.api_token).join(Notification).one()
    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect api-token",
        )
