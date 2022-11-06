from fastapi import FastAPI, Request, HTTPException
from schemas import Query
import config

import json, requests, smtplib, time, os.path, random, uvicorn

from email.mime.text import MIMEText


app = FastAPI()


@app.post("/api")
async def main(request: Request, query: Query):
    ip = request.client.host
    print(ip)
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

            response['time'] = str(time.strftime("%d/%m/%Y, %H:%M:%S", time.gmtime(time.time())))
            response['unix'] = time.time()
            await save_logs(response, source)

            return HTTPException(status_code=200, detail='OK')
    else:
        return HTTPException(status_code=403, detail='Forbidden')

async def save_logs(response, source):
    try:
        with open(f'''logs/{source['source']}.json''', 'r+') as f:
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
async def get_logs(request: Request, code: int = None, time_from: float = None, time_to: float = None):
    ip = request.client.host
    print(ip, code, time_from, time_to)
    if os.path.exists(f'logs/{ip}.json'):
        with open(f'logs/{ip}.json', 'r') as f:
            logs = json.load(f)
            result = {'logs': []}
            if code != None:
                for log in logs['logs']:
                    if time_from != None:
                        if time_to != None:
                            if log['code'] == code and time_from <= log['unix'] <= time_to:
                                result['logs'].append(log)
                        else:
                            if log['code'] == code and time_from <= log['unix']:
                                result['logs'].append(log)
                    elif time_to != None:
                        if log['code'] == code and time_to >= log['unix']:
                            result['logs'].append(log)
                    else:
                        if log['code'] == code:
                            result['logs'].append(log)
                return result
            elif time_from != None:
                for log in logs['logs']:
                    if time_to != None:
                        if time_from <= log['unix'] <= time_to:
                            result['logs'].append(log)
                    else:
                        if time_from <= log['unix']:
                            result['logs'].append(log)
                return result
            elif time_to != None:
                for log in logs['logs']:
                    if time_to >= log['unix']:
                        result['logs'].append(log)
                return result
            else:
                return logs
    else:
        with open('config.json', 'r') as f:
            sources = json.load(f)
            for source in sources['sources']:
                if source['source'] == ip:
                    return HTTPException(status_code=400, detail='You dont have any requests')
            else:
                return HTTPException(status_code=403, detail='Forbidden')