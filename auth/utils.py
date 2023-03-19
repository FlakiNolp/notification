from sqlalchemy.orm import Session
from auth.models import User, Notification
import hashlib


def get_user_by_email(email: str, db: Session):
    return db.query(User).where(User.email == email).one()