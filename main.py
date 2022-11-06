from datetime import datetime

from fastapi import FastAPI, Request, HTTPException, Query
from schemas import QueryModel
import config
from typing import List

import json, requests, smtplib, time, os.path, random

from email.mime.text import MIMEText


app = FastAPI()


@app.post("/api")
async def main(request: Request, query: QueryModel):
    ip = request.client.host
    with open('config.json', 'r') as f:
        sources = json.load(f)
    for source in sources['sources']:
        if source['source'] == ip:
            response = query.dict()
            text = f'''code: {response['code']}\nmessage: {response['message']}\nadditional: {response['additional']}'''

            if 'telegram' in source:
                try:
                    requests.get(f'''https://api.telegram.org/bot{config.telegram_api_key}/sendMessage?chat_id={source['telegram']}&text={text}''')
                except Exception as ex:
                    print(f'''Не получилось отправить сообщение {source['telegram']}\n{ex}''')

            if 'email' in source:
                    recipient = source['email']
                    await send_mail(recipient, text)

            if 'website' in source:
                try:
                    requests.post(f'''{source['website']}''', json=text)
                except Exception as ex:
                    print(f'''Не получилось отправить запрос на {source['website']}\n{ex}''')

            if 'vk' in source:
                try:
                    random_int = random.randint(1, 500)
                    random_id = str(int.from_bytes(bytes=(source['vk'] + config.vk_api_key).encode('utf-8'), byteorder='big'))[random_int: random_int + 9]
                    requests.get(f'''https://api.vk.com/method/messages.send?domain={source['vk']}&random_id={random_id}&message={text}&access_token={config.vk_api_key}&v=5.131''').json()
                except Exception as ex:
                    print(f'''Не получилось отправить сообщение {source['vk']}\n{ex}''')

            time_now = time.localtime(time.time())
            datetime(year=time_now.tm_year, month=time_now.tm_mon, day=time_now.tm_mday, hour=time_now.tm_hour, minute=time_now.tm_min, second=time_now.tm_sec)
            response['time'] = str(datetime(year=time_now.tm_year, month=time_now.tm_mon, day=time_now.tm_mday, hour=time_now.tm_hour, minute=time_now.tm_min, second=time_now.tm_sec))
            await save_logs(response, source)

            return HTTPException(status_code=200, detail='OK')
    else:
        return HTTPException(status_code=403, detail='Forbidden')

async def save_logs(response, source):
    try:
        with open(f'''logs/{source['source']}.json''', 'r') as f:
            logs_dict = json.load(f)
            logs_list = logs_dict['logs']
            logs_list.append(response)
            logs_dict = logs_dict
        with open(f'''logs/{source['source']}.json''', 'w+') as f:
            json.dump(logs_dict, f, ensure_ascii=False)
    except:
        logs_dict = {'logs': [response]}
        with open(f'''logs/{source['source']}.json''', 'w') as f:
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

@app.get('/api/logs')
async def get_logs(request: Request, code: List[int] = Query([int(i) for i in range(100, 527)], ge=100, le=526), time_from: datetime = datetime(year=1, month=1, day=1), time_to: datetime = datetime(year=9999, month=12, day=31)):
    ip = request.client.host
    if os.path.exists(f'logs/{ip}.json'):
        with open(f'logs/{ip}.json', 'r') as f:
            logs = json.load(f)
            result = {'logs': []}
            for log in logs['logs']:
                if log['code'] in code and time_from <= datetime.strptime(log['time'], '%Y-%m-%d %H:%M:%S') <= time_to:
                    result['logs'].append(log)
            return result
    else:
        with open('config.json', 'r') as f:
            sources = json.load(f)
            for source in sources['sources']:
                if source['source'] == ip:
                    return HTTPException(status_code=400, detail='You dont have any requests')
            else:
                return HTTPException(status_code=403, detail='Forbidden')