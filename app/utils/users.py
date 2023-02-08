from sqlalchemy.orm import Session
from app.models.users import User, Notification


def get_user_by_email(email: str, db: Session):
    return db.query(User).where(User.email == email).one()


def get_users(db: Session):
    return db.query(User).join(Notification.user).all()


def new_user(db: Session):
    user = User(id=1, email="user@example.ru", hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
                api_token="12345sakhdjgfsadkhfl264ocb8")
    notification = Notification(user_id=1, email="max@osetr.ru", telegram_id=12397123)
    db.add_all([user, notification])
    db.commit()
