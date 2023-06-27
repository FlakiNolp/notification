from datetime import datetime
import json
from typing import List

from fastapi import HTTPException, Query, APIRouter, BackgroundTasks, Depends, status
from fastapi.responses import JSONResponse, Response

from api.schemas import QueryModel
from api.utils.utils import notifications, get_hash_email

from api.utils.db_utils import get_user_email_by_api_token
from api.database.DataBase import DataBase
from api.database.models import Base

from sqlalchemy.orm import Session

router = APIRouter()

database = DataBase()
database.create_schema(Base)


@router.post("/api")
async def post_log(query: QueryModel, api_token: str, background_tasks: BackgroundTasks,
                   db: Session = Depends(database.get_db)):
    user = get_user_email_by_api_token(api_token=api_token, db=db)
    response = query.dict()
    background_tasks.add_task(notifications, user, response)
    return Response(status_code=status.HTTP_201_CREATED)


@router.get('/api/logs')
async def get_logs(api_token: str, db: Session = Depends(database.get_db),
                   code: List[int] = Query(None, ge=100, le=526),
                   time_from: datetime = None,
                   time_to: datetime = None,
                   message: List[str] = Query(None, min_length=1, max_length=100),
                   additional: List[str] = Query(None, min_length=1, max_length=100)):
    user = get_user_email_by_api_token(api_token=api_token, db=db)
    hash_filename = get_hash_email(user.email)
    try:
        with open(f'logs/{hash_filename}.json', 'r') as f:
            logs = json.load(f)
            result = []
            if message and additional and code:
                if time_from and time_to:
                    for log in logs['logs']:
                        if time_from <= datetime.strptime(log['time'], '%Y-%m-%d %H:%M:%S.%f') <=\
                                time_to and log['code'] in code and log['message'] in message\
                                and log['additional'] in additional:
                            result.append(log)
                elif time_from:
                    for log in logs['logs']:
                        if time_from <= datetime.strptime(log['time'], '%Y-%m-%d %H:%M:%S.%f') and log['code'] in code\
                                and log['message'] in message and log['additional'] in additional:
                            result.append(log)
                elif time_to:
                    for log in logs['logs']:
                        if time_to >= datetime.strptime(log['time'], '%Y-%m-%d %H:%M:%S.%f') and log['code'] in code\
                                and log['message'] in message and log['additional'] in additional:
                            result.append(log)
                else:
                    for log in logs['logs']:
                        if log['code'] in code and log['message'] in message and log['additional'] in additional:
                            result.append(log)
            elif message and additional:
                if time_from and time_to:
                    for log in logs['logs']:
                        if time_from <= datetime.strptime(log['time'], '%Y-%m-%d %H:%M:%S.%f') <= time_to\
                                and log['message'] in message and log['additional'] in additional:
                            result.append(log)
                elif time_from:
                    for log in logs['logs']:
                        if time_from <= datetime.strptime(log['time'], '%Y-%m-%d %H:%M:%S.%f')\
                                and log['message'] in message and log['additional'] in additional:
                            result.append(log)
                elif time_to:
                    for log in logs['logs']:
                        if time_to >= datetime.strptime(log['time'], '%Y-%m-%d %H:%M:%S.%f') \
                                and log['message'] in message and log['additional'] in additional:
                            result.append(log)
                else:
                    for log in logs['logs']:
                        if log['message'] in message and log['additional'] in additional:
                            result.append(log)
            elif message and code:
                if time_from and time_to:
                    for log in logs['logs']:
                        if time_from <= datetime.strptime(log['time'], '%Y-%m-%d %H:%M:%S.%f') <=\
                                time_to and log['code'] in code and log['message'] in message:
                            result.append(log)
                elif time_from:
                    for log in logs['logs']:
                        if time_from <= datetime.strptime(log['time'], '%Y-%m-%d %H:%M:%S.%f') and log['code'] in code\
                                and log['message'] in message:
                            result.append(log)
                elif time_to:
                    for log in logs['logs']:
                        if time_to >= datetime.strptime(log['time'], '%Y-%m-%d %H:%M:%S.%f') and log['code'] in code\
                                and log['message'] in message:
                            result.append(log)
                else:
                    for log in logs['logs']:
                        if log['code'] in code and log['message'] in message:
                            result.append(log)
            elif additional and code:
                if time_from and time_to:
                    for log in logs['logs']:
                        if time_from <= datetime.strptime(log['time'], '%Y-%m-%d %H:%M:%S.%f') <= \
                                time_to and log['code'] in code and log['message'] in message:
                            result.append(log)
                elif time_from:
                    for log in logs['logs']:
                        if time_from <= datetime.strptime(log['time'], '%Y-%m-%d %H:%M:%S.%f') and log['code'] in code \
                                and log['message'] in message:
                            result.append(log)
                elif time_to:
                    for log in logs['logs']:
                        if time_to >= datetime.strptime(log['time'], '%Y-%m-%d %H:%M:%S.%f') and log['code'] in code \
                                and log['message'] in message:
                            result.append(log)
                else:
                    for log in logs['logs']:
                        if log['code'] in code and log['message'] in message:
                            result.append(log)
            elif message:
                if time_from and time_to:
                    for log in logs['logs']:
                        if time_from <= datetime.strptime(log['time'], '%Y-%m-%d %H:%M:%S.%f') <= time_to\
                                and log['message'] in message:
                            result.append(log)
                elif time_from:
                    for log in logs['logs']:
                        if time_from <= datetime.strptime(log['time'], '%Y-%m-%d %H:%M:%S.%f') \
                                and log['message'] in message:
                            result.append(log)
                elif time_to:
                    for log in logs['logs']:
                        if time_to >= datetime.strptime(log['time'], '%Y-%m-%d %H:%M:%S.%f') \
                                and log['message'] in message:
                            result.append(log)
                else:
                    for log in logs['logs']:
                        if log['message'] in message:
                            result.append(log)
            elif additional:
                if time_from and time_to:
                    for log in logs['logs']:
                        if time_from <= datetime.strptime(log['time'], '%Y-%m-%d %H:%M:%S.%f') <= time_to\
                                and log['additional'] in additional:
                            result.append(log)
                elif time_from:
                    for log in logs['logs']:
                        if time_from <= datetime.strptime(log['time'], '%Y-%m-%d %H:%M:%S.%f') \
                                and log['additional'] in additional:
                            result.append(log)
                elif time_to:
                    for log in logs['logs']:
                        if time_to >= datetime.strptime(log['time'], '%Y-%m-%d %H:%M:%S.%f') \
                                and log['additional'] in additional:
                            result.append(log)
                else:
                    for log in logs['logs']:
                        if log['additional'] in additional:
                            result.append(log)
            elif code:
                if time_from and time_to:
                    for log in logs['logs']:
                        if time_from <= datetime.strptime(log['time'], '%Y-%m-%d %H:%M:%S.%f') <= time_to\
                                and log['code'] in code:
                            result.append(log)
                elif time_from:
                    for log in logs['logs']:
                        if time_from <= datetime.strptime(log['time'], '%Y-%m-%d %H:%M:%S.%f') \
                                and log['code'] in code:
                            result.append(log)
                elif time_to:
                    for log in logs['logs']:
                        if time_to >= datetime.strptime(log['time'], '%Y-%m-%d %H:%M:%S.%f') \
                                and log['code'] in code:
                            result.append(log)
                else:
                    for log in logs['logs']:
                        if log['code'] in code:
                            result.append(log)
            else:
                if time_from and time_to:
                    for log in logs['logs']:
                        if time_from <= datetime.strptime(log['time'], '%Y-%m-%d %H:%M:%S.%f') <= time_to:
                            result.append(log)
                elif time_from:
                    for log in logs['logs']:
                        if time_from <= datetime.strptime(log['time'], '%Y-%m-%d %H:%M:%S.%f'):
                            result.append(log)
                elif time_to:
                    for log in logs['logs']:
                        if time_to >= datetime.strptime(log['time'], '%Y-%m-%d %H:%M:%S.%f'):
                            result.append(log)
                else:
                    for log in logs['logs']:
                        result.append(log)
            result = JSONResponse(content=result, media_type="application/json")
            return result
    except FileNotFoundError:
        return HTTPException(status_code=400, detail='You dont have any requests')
