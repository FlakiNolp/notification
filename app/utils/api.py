import json
import smtplib
from app import config
from email.mime.text import MIMEText


async def save_logs(response, source):
    try:
        with open(f'''logs/{source[0]}.json''', 'r') as f:
            logs_dict = json.load(f)
            logs_list = logs_dict['logs']
            logs_list.append(response)
            logs_dict = logs_dict
        with open(f'''logs/{source[0]}.json''', 'w+') as f:
            json.dump(logs_dict, f, ensure_ascii=False)
    except:
        logs_dict = {'logs': [response]}
        with open(f'''logs/{source[0]}.json''', 'w') as f:
            json.dump(logs_dict, f, ensure_ascii=False)


async def send_mail(recipient, text):
    sender = 'check.telegram.bot@gmail.com'
    password = f'{config.email_password}'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEText(f'{text}')
        msg['Subject'] = 'Error notification'
        server.sendmail(sender, recipient, msg.as_string())

        print(f'Письмо успешно отправлено на {recipient}')

    except Exception as ex:
        print(f'Не получилось отправить письмо {recipient}\n{ex}')