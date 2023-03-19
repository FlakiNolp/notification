from fastapi.testclient import TestClient
from fastapi import Depends
from api.main import app
from api.database import get_db
from sqlalchemy.orm import Session
from api.utils import get_hash_email
import os
from api import config
from api.models import User, Notification
import pytest
from httpx import AsyncClient

client = TestClient(app)


# @pytest.mark.anyio
# async def test_api_logs():
#    request_data = {
#        "code": 228,
#        "message": "Hu",
#        "additional": "Hi"
#    }
#    async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
#        for _ in range(100):
#            await ac.post('/api?api_token=372862815856933:71cb2613537fefa1d11b6f358dc91ce42afbae68394257a5c3b9838542c0da36', json=request_data)


def test_api_save_logs(db=Depends(get_db)):
    request_data = {
        "code": 526,
        "message": "test_message",
        "additional": "test_additional"
    }
    os.curdir = config.logs_path
    os.system(rf'rd {os.curdir} /S /Q')
    os.system(rf"md {os.curdir}")
    api_token = "3217649459838867:50221e4fc0d7db216c62c553fc70fabb48d1c571f50b5215dd4c89df7bae57e1"
    client.post(f"/api?api_token={api_token}",
                json=request_data)
    client.post(f"/api?api_token={api_token}",
                json=request_data)
    client.post(f"/api?api_token={api_token}1",
                json=request_data)

    query_database(api_token, db, "maksimosetrov4@gmail.com", 822871873, "osetr4", "https://vk.com")
    client.post(f"/api?api_token={api_token}",
                json=request_data)

    query_database(api_token, db)
    client.post(f"/api?api_token={api_token}",
                json=request_data)

    query_database(api_token, db, "sdfld", 1, "sdfkjdshflskdjcljasdfxajdhf", "asdmnaxsasd")
    client.post(f"/api?api_token={api_token}",
                json=request_data)


def query_database(api_token: str, db: Session, email=None, telegram_id: int = None, vk_domain=None, website=None):

    user = db.query(User).where(User.api_token == api_token).join(Notification). \
        where(Notification.user_id == User.id).one()
    user.services.email = email
    user.services.telegram_id = telegram_id
    user.services.vk_domain = vk_domain
    user.services.website = website
    db.commit()
