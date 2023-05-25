from fastapi.testclient import TestClient

from sqlalchemy.engine import create_engine
from sqlalchemy import URL
from os import getenv
import os
from sqlalchemy.orm import sessionmaker, Session

from api.database.models import Base, User, Notification
from api.start_server import app
from api.database import get_db
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


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_api_save_logs(db=override_get_db()):
    os.curdir = 'test_' + config.LOGS_PATH
    os.system('rd test_' + f'{os.curdir} /S /Q')
    os.system('md test_' + f'{os.curdir}')

    create_user(db)

    client.post(f"/api?api_token=8802824020385742:d0e7f6bf-07f8-485d-b439-73a9e1ca55eb",
                json={'code': 100, 'message': 'test_message', 'additional': 'test_additional'})
    #client.post(f"/api?api_token=8802824020385742:d0e7f6bf-07f8-485d-b439-73a9e1ca55eb",
    #            json={'code': 101, 'message': 'test_message'})
    #client.post(f"/api?api_token=8802824020385742:d0e7f6bf-07f8-485d-b439-73a9e1ca55eb",
    #            json={'code': 102, 'additional': 'test_additional'})
    #client.post(f"/api?api_token=8802824020385742:d0e7f6bf-07f8-485d-b439-73a9e1ca55eb",
    #            json={'code': 103, 'message': 'test_message', 'additional': 'test_additional'})


def create_user(db: Session):
    user = User(id=1, email='maksimosetrov4@gmail.com',
                hashed_password='2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b',
                api_token='8802824020385742:d0e7f6bf-07f8-485d-b439-73a9e1ca55eb')
    services = Notification(user_id=1, email='maksimosetrov4@gmail.com', telegram_id=822871873, vk_domain='osetr4',
                            website='http://localhost:1002')
    db.add_all([user, services])
    db.commit()
