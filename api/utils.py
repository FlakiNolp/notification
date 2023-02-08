import json
import smtplib
from api import config
from email.mime.text import MIMEText
import hashlib
import asyncio
import random
import time
from datetime import datetime
import requests


def get_hash_api_token(api_token: str):
    return hashlib.sha256(api_token.encode()).hexdigest()


async def save_logs(response, source):
    time_now = time.localtime(time.time())
    response['time'] = str(
        datetime(year=time_now.tm_year, month=time_now.tm_mon, day=time_now.tm_mday, hour=time_now.tm_hour,
                 minute=time_now.tm_min, second=time_now.tm_sec, microsecond=int(time.time() % 1 * 1000000)))
    try:
        with open(f'''{config.logs_path}/{source}.json''', 'r') as f:
            logs_dict = json.load(f)
            logs_list = logs_dict['logs']
            logs_list.append(response)
            logs_dict = logs_dict
        with open(f'''{config.logs_path}/{source}.json''', 'w+') as f:
            json.dump(logs_dict, f, ensure_ascii=False)
    except:
        logs_dict = {'logs': [response]}
        with open(f'''{config.logs_path}/{source}.json''', 'a+') as f:
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


async def send_telegram(recipient, text):
    try:
        requests.get(f'''https://api.telegram.org/bot{config.telegram_api_key}/sendMessage?chat_id={recipient}&text={text}''')
    except Exception as ex:
         print(f'''Не получилось отправить сообщение {recipient}\n{ex}''')


async def send_vk(recipient, text):
    try:
        random_int = random.randint(1, 500)
        random_id = str(
            int.from_bytes(bytes=(recipient + config.vk_api_key).encode('utf-8'), byteorder='big'))[
                    random_int: random_int + 9]
        requests.get(f'''https://api.vk.com/method/messages.send?domain={recipient}&random_id={random_id}&message={text}&access_token={config.vk_api_key}&v=5.131''')
    except Exception as ex:
        print(f'''Не получилось отправить сообщение {recipient}\n{ex}''')


async def send_website(recipient: str, text: str):
    try:
        requests.post(f'''{recipient}''', json=text)
    except Exception as ex:
        print(f'''Не получилось отправить запрос на {recipient}\n{ex}''')


async def notifications(user, response: dict):
    text = f'''code: {response['code']}\nmessage: {response['message']}\nadditional: {response['additional']}'''
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(save_logs(response=response, source=get_hash_api_token(user.api_token)))
        if user.services.email is not None:
            task2 = tg.create_task(send_mail(recipient=user.services.email, text=text))
        if user.services.telegram_id is not None:
            task3 = tg.create_task(send_telegram(recipient=user.services.telegram_id, text=text))
        if user.services.vk_domain is not None:
            task4 = tg.create_task(send_vk(recipient=user.services.vk_domain, text=text))
        if user.services.website is not None:
            task5 = tg.create_task(send_website(recipient=user.services.website, text=text))
