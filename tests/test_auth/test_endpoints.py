from auth.database.DataBase import DataBase
from auth.start_server import app
from auth.database.models import User, Notification
from auth.routers.tokens import database

from tests.context_manager_class import DependencyOverrider

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

override_database = DataBase(test_mode=True)
override_database.create_schema()


@pytest.fixture(scope='function')
def client_auth():
    with TestClient(app=app, base_url='http://localhost:1000') as client:
        yield client


@pytest.fixture(scope='function')
def set_override_test_db():
    with DependencyOverrider(app, overrides={database.get_db: override_database.get_db}) as overrider:
        yield overrider


def test_routers(client_auth, set_override_test_db, db: Session = next(override_database.get_db())):
    db.query(User).delete()
    db.commit()

    user = User(email='test@example.com',
                hashed_password='2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b',
                api_token='1').services = Notification()

    db.add(user)

    response_true = client_auth.post('/token', data={'username': 'test@example.com', 'password': 'secret'})
    response_false = client_auth.post('/token', data={'username': 'test@example.com', 'password': 'secret1'})

    response_refresh_true = client_auth.post('/refresh', cookies={'refresh_token': response_true.json().refresh_token})
    response_refresh_false = client_auth.post('/refresh', cookies={'refresh_token': response_true.json().refresh_token})

    assert response_true.status_code == 200
    assert response_false.status_code == 401
    assert response_refresh_true.status_code == 200
    assert response_refresh_false.status_code == 401
