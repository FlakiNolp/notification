import sqlalchemy.exc

from api.models import User, Notification
from sqlalchemy.orm import Session
from api.utils import get_hash_api_token
from fastapi import status, HTTPException


def get_user_by_api_token(api_token: str, db: Session):
    try:
        return db.query(User).join(Notification).where(get_hash_api_token(api_token) == User.api_token).one()
    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect api-token",
        )
    except Exception as e:
        return e
