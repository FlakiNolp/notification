import requests
import time
from datetime import datetime
import random
import json
import os
from typing import List

from fastapi import Request, HTTPException, Query, APIRouter, BackgroundTasks

from app import config
from app.utils.db import db
from app.schemas.api import QueryModel
from app.utils.api import save_logs, send_mail

router = APIRouter()


@router.post("/api")
async def post_log(request: Request, query: QueryModel, api_key: str = Query(...)):
    print(api_key)
    ip = request.client.host
    sources = await db.get_all_sources()
    for source in sources:
        if source[0] == ip:
            source = await db.get_user(source[0])
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


@router.get('/api/logs')
async def get_logs(request: Request, code: List[int] = Query([int(i) for i in range(100, 527)], ge=100, le=526), time_from: datetime = datetime(year=1, month=1, day=1), time_to: datetime = datetime(year=9999, month=12, day=31), message: List[str] = Query(None, min_length=1, max_length=100), additional: List[str] = Query(None, min_length=1, max_length=100)):
    ip = request.client.host
    if os.path.exists(f'{config.logs_path}/{ip}.json'):
        with open(f'{config.logs_path}/{ip}.json', 'r') as f:
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