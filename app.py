from datetime import datetime

from fastapi import FastAPI, Request, HTTPException, Query, Form
from fastapi.templating import Jinja2Templates
from schemas import QueryModel
import config
from typing import List

import json, requests, smtplib, time, os.path, random

from email.mime.text import MIMEText

from db import DataBase

db = DataBase('users.db')
app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.post("/api")
async def post_log(request: Request, query: QueryModel):
    ip = request.client.host
    sources = await db.get_all_sources()
    for source in sources:
        if source[0] == ip:
            source = await db.get_user(source[0])
            #print(source)
            print(source[0], source[1], source[2], source[3], source[4])
            response = query.dict()
            text = f'''code: {response['code']}\nmessage: {response['message']}\nadditional: {response['additional']}'''
            if source[2] is not None:
                try:
                    requests.get(f'''https://api.telegram.org/bot{config.telegram_api_key}/sendMessage?chat_id={source[2]}&text={text}''')
                except Exception as ex:
                    print(f'''Не получилось отправить сообщение {source[2]}\n{ex}''')

            if source[1] is not None:
                    recipient = source[1]
                    await send_mail(recipient, text)

            if source[4] is not None:
                try:
                    requests.post(f'''{source[4]}''', json=text)
                except Exception as ex:
                    print(f'''Не получилось отправить запрос на {source['website']}\n{ex}''')

            if source[3] is not None:
                try:
                    random_int = random.randint(1, 500)
                    random_id = str(int.from_bytes(bytes=(source[3] + config.vk_api_key).encode('utf-8'), byteorder='big'))[random_int: random_int + 9]
                    requests.get(f'''https://api.vk.com/method/messages.send?domain={source[3]}&random_id={random_id}&message={text}&access_token={config.vk_api_key}&v=5.131''').json()
                except Exception as ex:
                    print(f'''Не получилось отправить сообщение {source[3]}\n{ex}''')

            time_now = time.localtime(time.time())
            datetime(year=time_now.tm_year, month=time_now.tm_mon, day=time_now.tm_mday, hour=time_now.tm_hour, minute=time_now.tm_min, second=time_now.tm_sec)
            response['time'] = str(datetime(year=time_now.tm_year, month=time_now.tm_mon, day=time_now.tm_mday, hour=time_now.tm_hour, minute=time_now.tm_min, second=time_now.tm_sec))
            await save_logs(response, source)

            return HTTPException(status_code=200, detail='OK')
    else:
        return HTTPException(status_code=403, detail='Forbidden')


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


@app.get('/api/logs')
async def get_logs(request: Request, code: List[int] = Query([int(i) for i in range(100, 527)], ge=100, le=526), time_from: datetime = datetime(year=1, month=1, day=1), time_to: datetime = datetime(year=9999, month=12, day=31), message: List[str] = Query(None, min_length=1, max_length=100), additional: List[str] = Query(None, min_length=1, max_length=100)):
    ip = request.client.host
    if os.path.exists(f'logs/{ip}.json'):
        with open(f'logs/{ip}.json', 'r') as f:
            logs = json.load(f)
            result = {'logs': []}
            if message and additional:
                for log in logs['logs']:
                    if log['code'] in code and time_from <= datetime.strptime(log['time'], '%Y-%m-%d %H:%M:%S') <= time_to and log['message'] in message and log['additional'] in additional:
                        result['logs'].append(log)
            elif message:
                for log in logs['logs']:
                    if log['code'] in code and time_from <= datetime.strptime(log['time'], '%Y-%m-%d %H:%M:%S') <= time_to and log['message'] in message:
                        result['logs'].append(log)
            elif additional:
                for log in logs['logs']:
                        if log['code'] in code and time_from <= datetime.strptime(log['time'], '%Y-%m-%d %H:%M:%S') <= time_to and log['additional'] in additional:
                            result['logs'].append(log)
            else:
                for log in logs['logs']:
                        if log['code'] in code and time_from <= datetime.strptime(log['time'], '%Y-%m-%d %H:%M:%S') <= time_to:
                            result['logs'].append(log)
            return result
    else:
        sources = await db.get_all_sources()
        for source in sources:
            if source[0] == ip:
                return HTTPException(status_code=400, detail='You dont have any requests')
        else:
            return HTTPException(status_code=403, detail='Forbidden')


@app.get('/settings')
async def settings(request: Request):
    if request.client.host == '(ip админа)':
        return templates.TemplateResponse('settings.html', context={"request": request}, status_code=200)
    else:
        return HTTPException(status_code=403, detail='Forbidden')


@app.get('/settings/delete')
async def settings_delete_get(request: Request):
    if request.client.host == '(ip админа)':
        all_sources = await db.get_all_sources()
        return templates.TemplateResponse('delete.html', context={'request': request, 'sources': all_sources}, status_code=200)
    else:
        return HTTPException(status_code=403, detail='Forbidden')


@app.post('/settings/delete')
async def settings_delete_post(request: Request, source: str = Form()):
    if request.client.host == '(ip админа)':
        all_sources = await db.get_all_sources()
        try:
            await db.delete_user(source)
            return templates.TemplateResponse('delete.html', context={'request': request, 'sources': all_sources, 'status': 'Удален'}, status_code=200)
        except Exception as ex:
            return templates.TemplateResponse('delete.html', context={'request': request, 'sources': all_sources, 'status': ex }, status_code=200)
    else:
        return HTTPException(status_code=403, detail='Forbidden')


@app.get('/settings/add')
async def settings_add_get(request: Request):
    if request.client.host == (ip админа)':
        return templates.TemplateResponse('add.html', context={"request": request}, status_code=200)
    else:
        return HTTPException(status_code=403, detail='Forbidden')

@app.post('/settings/add')
async def settings_add_post(request: Request, source: str = Form(), telegram: str = Form(None), email: str = Form(None), vk: str = Form(None), website: str = Form(None)):
    if request.client.host == '(ip админа)':
        try:
            await db.add_new_user(source=source, email=email, telegram=telegram, vk=vk, website=website)
            return templates.TemplateResponse('add.html', context={"request": request, "status": 'Добавлен'}, status_code=200)
        except Exception as ex:
            return templates.TemplateResponse('add.html', context={"request": request, "status": ex}, status_code=200)
    else:
        return HTTPException(status_code=403, detail='Forbidden')

@app.get('/settings/edit')
async def settings_edit_pick_get(request: Request):
    if request.client.host == '(ip админа)':
        all_sources = await db.get_all_sources()
        return templates.TemplateResponse('edit.html', context={'request': request, 'sources': all_sources}, status_code=200)
    else:
        return HTTPException(status_code=403, detail='Forbidden')

@app.post('/settings/edit')
async def settings_edit_get(request: Request, source: str = Form(), telegram: str = Form(None), email: str = Form(None), vk: str = Form(None), website: str = Form(None)):
    if request.client.host == '(ip админа)':
        all_sources = await db.get_all_sources()
        try:
            user = (await db.get_user(source=source))[1:]
            services = [email, telegram, vk, website]
            for i in range(3):
                if user[i] is not None:
                    services[i] = user[i]
            await db.edit_user(source=source, email=services[0], telegram=services[1], vk=services[2], website=services[3])
            return templates.TemplateResponse('edit.html', context={'request': request, 'sources': all_sources, 'status': 'Изменен'}, status_code=200)
        except Exception as ex:
            return templates.TemplateResponse('edit.html', context={'request': request, 'sources': all_sources, 'status': ex}, status_code=200)
    else:
        return HTTPException(status_code=403, detail='Forbidden')