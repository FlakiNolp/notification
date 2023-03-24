import hashlib
from datetime import timedelta
from app.config import EMAIL_PASSWORD, HOST_DOMAIN
from app.utils.aunth import create_token
import smtplib
from email.mime.text import MIMEText
from sqlalchemy.orm import Session
import app.utils.db_utils as db_utils


def get_hash(plain: str):
    return hashlib.sha256(plain.encode()).hexdigest()


def send_mail(recipient, text):
    sender = 'check.telegram.bot@gmail.com'
    password = f'{EMAIL_PASSWORD}'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEText(f'{text}')
        msg['Subject'] = 'Error notification'
        server.sendmail(sender, recipient, msg.as_string())
    except:
        return False


def send_token_email(email, password):
    expire_delta = timedelta(minutes=10)
    encoded_jwt = create_token({"email": email, "hashed_password": password}, expire_delta)
    #text = f"Перейдите по ссылке, чтобы завершить процесс регистрации\n\nhttp://127.0.0.1:1002/registration?email_token={encoded_jwt}\n\nСсылка действительна 10 минут"
    text = f"http://{HOST_DOMAIN}:1002/registration?token={encoded_jwt}"
    if not send_mail(email, text):
        return False


def send_token_update_password(db: Session, user_id: int):
    expire_delta = timedelta(minutes=10)
    encoded_jwt = create_token({"id": user_id}, expire_delta)
    email = db_utils.get_email_by_id(user_id, db)
    #text = f"Пройдите по ссылке, чтобы поменять пароль\n\nhttp://127.0.0.1:1002/new_password?email_token={encoded_jwt}\n\nСсылка действительна 10 минут"
    text = f"http://{HOST_DOMAIN}:1002/me/new-password?token={encoded_jwt}"
    if not send_mail(email, text):
        return False