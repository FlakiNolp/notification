from app.start_server import app
from app.database.connection import get_db
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from sqlalchemy.engine import create_engine
from sqlalchemy import URL
from os import getenv
from sqlalchemy.orm import sessionmaker, Session
from app.database.models import Base

from app.utils.auth import create_token
from app.database.models import User, Notification

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
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.mark.anyio
async def test_speed():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:1002") as ac:
        response1 = await ac.post("/sign-up", headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                  data={"username": "maksimosetrov4@gmail.com", "password": "super_secret"})
        response3 = await ac.get(
            "/registration?email_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1ha3NpbW9zZXRyb3Y0QGdtYWlsLmNvbSIsImhhc2hlZF9wYXNzd29yZCI6IjVjMGI2MmViNWZiMzA4N2FmY2U3ZTliYWM0ZTA2NjExMTliZDYyNzg1MzBmNTY4MzNmOGVlMTg5MDM0MzZjYWUiLCJleHAiOjE2NzcwMTU4NDl9.k4SBBGpSsuII-dgY_VMYQMeEJQDGEpqvf8BNuHOh2Ak")
        response2 = await ac.post("/sign-up", headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                  data={"username": "maxim.osetrov-2016@yandex.ru", "password": "secret"})
        response4 = await ac.get(
            "/registration?email_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1heGltLm9zZXRyb3YtMjAxNkB5YW5kZXgucnUiLCJoYXNoZWRfcGFzc3dvcmQiOiIyYmI4MGQ1MzdiMWRhM2UzOGJkMzAzNjFhYTg1NTY4NmJkZTBlYWNkNzE2MmZlZjZhMjVmZTk3YmY1MjdhMjViIiwiZXhwIjoxNjc3MDE1ODUwfQ.OMSPi-mSBuFS_T3U7WtVoNEvf3osJbqnmdm8nvg-gco")
        print(response1, response2, response3, response4)


def test_registration(db: Session = override_get_db()):
    response = client.post("/sign-up", headers={'Content-Type': 'application/x-www-form-urlencoded'},
                           data={"username": "maksimosetrov4@gmail.com", "password": "super_secret"})
    token = create_token({"username": "maksimosetrov4@gmail.com", "password": "super_secret"}, 10)
    assert response.status_code == 200

    response_reg = client.get(f"/registration?email_token={token}")
    result_db = db.query(User).where(User.email == "maksimosetrov4@gmail.com").one()
    assert response_reg.status_code == 301 and result_db
