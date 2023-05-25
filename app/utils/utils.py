import hashlib
from app.config import EMAIL_PASSWORD, HOST_DOMAIN
from app.utils.auth import create_token
import smtplib
from email.mime.text import MIMEText
from sqlalchemy.orm import Session
import app.utils.db_utils as db_utils


def get_hash(plain: str):
    return hashlib.sha256(plain.encode()).hexdigest()


def send_mail(recipient, text):
    sender = 'noreply@osetr.space'
    server = smtplib.SMTP('smtp.mail.ru', 587)
    server.starttls()

    try:
        server.login(sender, EMAIL_PASSWORD)
        msg = MIMEText(f'{text}')
        msg['Subject'] = 'Error notification'
        server.sendmail(sender, recipient, msg.as_string())
    except Exception as e:
        print(e)
        return False


def send_token_email(email, password):
    encoded_jwt = create_token({"email": email, "hashed_password": password}, 10)
    #text = f"��������� �� ������, ����� ��������� ������� �����������\n\nhttp://127.0.0.1/registration?email_token={encoded_jwt}\n\n������ ������������� 10 �����"
    text = f"http://{HOST_DOMAIN}/registration?token={encoded_jwt}"
    if not send_mail(email, text):
        return False


def send_token_update_password(db: Session, user_id: int):
    encoded_jwt = create_token({"id": user_id}, 10)
    email = db_utils.get_email_by_id(user_id, db)
    #text = f"�������� �� ������, ����� �������� ������\n\nhttp://127.0.0.1/new_password?email_token={encoded_jwt}\n\n������ ������������� 10 �����"
    text = f"http://{HOST_DOMAIN}/me/new-password?token={encoded_jwt}"
    if not send_mail(email, text):
        return False