from fastapi.testclient import TestClient

from httpx import AsyncClient
import pytest
import asyncio

from sqlalchemy.engine import create_engine
from sqlalchemy import URL
from os import getenv
import os
from sqlalchemy.orm import sessionmaker, Session

from api.database.models import Base, User, Notification
from api.start_server import app
#from api.database import get_db
from api import config

db_user = getenv("DB_USER", "postgres")
db_password = getenv("DB_PASSWORD")
db_host = getenv("DB_HOST", "localhost")
db_port = getenv("DB_PORT", 6543)

url = URL.create(drivername="postgresql+psycopg2", username=db_user, password=db_password, host=db_host, port=db_port,
                 database="users")

engine = create_engine(url)

Base.metadata.create_all(engine)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


#app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_api_save_logs(db=override_get_db()):
    os.curdir = 'test_' + config.LOGS_PATH
    os.system('rd test_' + f'{os.curdir} /S /Q')
    os.system('md test_' + f'{os.curdir}')

    create_user(db)

    response = client.post(f"/api?api_token=8802824020385742:d0e7f6bf-07f8-485d-b439-73a9e1ca55eb",
                json={'code': 123, 'message': 'test_message', 'additional': 'test_additional'})
    # client.post(f"/api?api_token=8802824020385742:d0e7f6bf-07f8-485d-b439-73a9e1ca55eb",
    #            json={'code': 101, 'message': 'test_message'})
    # client.post(f"/api?api_token=8802824020385742:d0e7f6bf-07f8-485d-b439-73a9e1ca55eb",
    #            json={'code': 102, 'additional': 'test_additional'})
    # client.post(f"/api?api_token=8802824020385742:d0e7f6bf-07f8-485d-b439-73a9e1ca55eb",
    #            json={'code': 103, 'message': 'test_message', 'additional': 'test_additional'})


@pytest.mark.anyio
async def test_spam():
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        async with asyncio.TaskGroup() as tg:
            for i in range(100):
                if i % 3 == 3:
                    response = await tg.create_task(
                        get_post_response(ac, "/api?api_token=5282769203186035:8c4ad0e8-e9f2-454d-a3d7-9609da136ac4",
                                          json={'code': 124, 'message': 'test_message',
                                                'additional': 'test_additional'}))
                elif i % 3 == 2:
                    response = await tg.create_task(
                        get_post_response(ac, "/api?api_token=3434715270996094:7b3d02c9-6eb9-4baf-884d-2aefe1969227",
                                          json={'code': 124, 'message': 'test_message',
                                                'additional': 'test_additional'}))
                else:
                    response = await tg.create_task(
                        get_post_response(ac, "/api?api_token=7609896659851074:9edebb4e-3e0f-49a4-8ee7-a6c5827f0d35",
                                          json={'code': 124, 'message': 'test_message',
                                                'additional': 'test_additional'}))
    assert response.status_code == 201


async def get_post_response(ac: AsyncClient(), url: str, json: dict):
    return await ac.post(url, json=json)


def create_user(db: Session):
    user = User(id=1, email='maksimosetrov4@gmail.com',
                hashed_password='2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b',
                api_token='8802824020385742:d0e7f6bf-07f8-485d-b439-73a9e1ca55eb')
    services = Notification(user_id=1, email='maksimosetrov4@gmail.com', telegram_id=822871873, vk_domain='osetr4',
                            website='http://localhost:1002')
    db.add_all([user, services])
    db.commit()
