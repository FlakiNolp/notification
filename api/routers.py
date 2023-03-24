from datetime import datetime
import json
from typing import List

from fastapi import HTTPException, Query, APIRouter, BackgroundTasks, Depends, status
from fastapi.responses import JSONResponse, Response

from api.schemas import QueryModel
from api.utils import notifications, get_hash_email

from api.db_utils import get_user_email_by_api_token
from api.database import get_db

from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/api")
async def post_log(query: QueryModel, api_token: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = get_user_email_by_api_token(api_token=api_token, db=db)
    response = query.dict()
    background_tasks.add_task(notifications, user, response)
    return Response(status_code=status.HTTP_201_CREATED)


@router.get('/api/logs')
async def get_logs(api_token: str, db: Session = Depends(get_db),
                   code: List[int] = Query([int(i) for i in range(100, 527)], ge=100, le=526),
                   time_from: datetime = datetime(year=1, month=1, day=1),
                   time_to: datetime = datetime(year=9999, month=12, day=31),
                   message: List[str] = Query(None, min_length=1, max_length=100),
                   additional: List[str] = Query(None, min_length=1, max_length=100)):
    user = get_user_email_by_api_token(api_token=api_token, db=db)
    hash_filename = get_hash_email(user.email)
    try:
        with open(f'logs/{hash_filename}.json', 'r') as f:
            logs = json.load(f)
            result = {'logs': []}
            if message and additional:
                for log in logs['logs']:
                    if log['code'] in code and time_from <= datetime.strptime(log['time'], '%Y-%m-%d %H:%M:%S.%f') <=\
                            time_to and log['message'] in message and log['additional'] in additional:
                        result['logs'].append(log)
            elif message:
                for log in logs['logs']:
                    if log['code'] in code and time_from <= datetime.strptime(log['time'], '%Y-%m-%d %H:%M:%S.%f') <=\
                            time_to and log['message'] in message:
                        result['logs'].append(log)
            elif additional:
                for log in logs['logs']:
                    if log['code'] in code and time_from <= datetime.strptime(log['time'], '%Y-%m-%d %H:%M:%S.%f') <=\
                            time_to and log['additional'] in additional:
                        result['logs'].append(log)
            else:
                for log in logs['logs']:
                    if log['code'] in code and time_from <= datetime.strptime(log['time'], '%Y-%m-%d %H:%M:%S.%f') <=\
                            time_to:
                        result['logs'].append(log)
            result = JSONResponse(content=result, media_type="application/json")
            return result
    except FileNotFoundError:
        return HTTPException(status_code=400, detail='You dont have any requests')

