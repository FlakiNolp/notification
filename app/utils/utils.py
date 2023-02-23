import hashlib
from datetime import timedelta
from app.config import email_password
from app.utils.aunth import create_email_token
import smtplib
from email.mime.text import MIMEText


def get_hash(plain: str):
    return hashlib.sha256(plain.encode()).hexdigest()


async def send_mail(recipient, text):
    sender = 'check.telegram.bot@gmail.com'
    password = f'{email_password}'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEText(f'{text}')
        msg['Subject'] = 'Error notification'
        server.sendmail(sender, recipient, msg.as_string())
    except:
        return False


async def send_token_email(email, password):
    expire_delta = timedelta(minutes=10)
    encoded_jwt = create_email_token({"email": email, "hashed_password": password}, expire_delta)

    #text = f"ѕерейдите по ссылке, чтобы завершить процесс регистрации\n\nhttp://127.0.0.1:1002/registration?email_token={encoded_jwt}\n\n—сылка действительна 10 минут"
    text = f"http://127.0.0.1:1002/registration?email_token={encoded_jwt}"
    if not await send_mail(email, text):
        return False
