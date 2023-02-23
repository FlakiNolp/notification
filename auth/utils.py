from sqlalchemy.orm import Session
from auth.models import User, Notification
import hashlib


def get_user_by_email(email: str, db: Session):
    return db.query(User).where(User.email == email).one()


def new_user(db: Session):
    user = User(id=1, email="maxim.osetrov-2016@yandex.ru", hashed_password=f'{hashlib.sha256(b"secret").hexdigest()}',
                api_token=f'''{hashlib.sha256("you_api_token".encode()).hexdigest()}''')
    notification = Notification(user_id=1, email="maksimosetrov4@gmail.com")
    db.add_all([user, notification])
    db.commit()