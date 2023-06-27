from api.database.DataBase import DataBase
from api.start_server import app
from api.database.models import User, Notification
from api.routers.api import database
from api.utils.utils import get_hash_email

from tests.context_manager_class import DependencyOverrider

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import json
import os

override_database = DataBase(test_mode=True)
override_database.create_schema()


@pytest.fixture(scope='function')
def client_api():
    with TestClient(app=app, base_url='http://localhost:1001') as client:
        yield client


@pytest.fixture(scope='function')
def set_override_test_db():
    with DependencyOverrider(
            app, overrides={database.get_db: override_database.get_db}
    ) as overrider:
        yield overrider


def test_post_logs(client_api, set_override_test_db, db: Session = next(override_database.get_db())):
    db.query(User).delete()
    db.commit()

    user_without_services = User(email='test@example.com', hashed_password='secret',
                                 api_token='1').services = Notification()

    user_with_services = (User(email='test2@example.com', hashed_password='secret', api_token='2')
                          ).services = Notification(email='mvosetrov@edu.hse.ru', telegram_id=822871873,
                                                    vk_domain='osetr4',
                                                    website='https://vk.com')

    user_with_wrong_services = (User(email='test3@example.com', hashed_password='secret', api_token='3')
                                ).services = Notification(email='dsfgdfg', telegram_id=1,
                                                          vk_domain='78902347890234789023478024789',
                                                          website='sdfgfdg')

    db.add_all((user_without_services, user_with_services, user_with_wrong_services))
    db.commit()

    response1_without_services = client_api.post('/api?api_token=1', json={'code': 123, 'message': 'm',
                                                                           'additional': 'a'})
    response2_without_services = client_api.post('/api?api_token=1', json={'code': 124, 'message': 'm',
                                                                           'additional': 'a'})

    response1_with_services = client_api.post('/api?api_token=2', json={'code': 123, 'message': 'm',
                                                                        'additional': 'a'})

    response1_with_wrong_services = client_api.post('/api?api_token=3', json={'code': 123, 'message': 'm',
                                                                              'additional': 'a'})

    assert response1_without_services.status_code == 201
    assert response1_with_services.status_code == 201
    assert response2_without_services.status_code == 201
    assert response1_with_wrong_services.status_code == 201

    with open(f'''../../tests/test_api/logs/{get_hash_email('test@example.com')}.json''') as f:
        logs = json.load(f)['logs']
        logs1 = logs[0]
        logs2 = logs[1]
        assert logs1['code'] == 123 and logs1['message'] == 'm' and logs1['additional'] == 'a'
        assert logs2['code'] == 124 and logs2['message'] == 'm' and logs2['additional'] == 'a'
    os.remove(f'''../../tests/test_api/logs/{get_hash_email('test@example.com')}.json''')

    with open(f'''../../tests/test_api/logs/{get_hash_email('test2@example.com')}.json''') as f:
        logs = json.load(f)['logs'][0]
        assert logs['code'] == 123 and logs['message'] == 'm' and logs['additional'] == 'a'
    os.remove(f'''../../tests/test_api/logs/{get_hash_email('test2@example.com')}.json''')

    os.remove(f'''../../tests/test_api/logs/{get_hash_email('test3@example.com')}.json''')


def test_get_logs(client_api, set_override_test_db, db: Session = next(override_database.get_db())):
    db.query(User).delete()
    db.commit()

    user_without_services = User(email='test@example.com', hashed_password='secret',
                                 api_token='1').services = Notification()

    db.add(user_without_services)
    db.commit()

    response_get_null = client_api.get('/api/logs', params={'api_token': '1'})
    client_api.post('/api?api_token=1', json={'code': 123, 'message': 'm',
                                              'additional': 'a'})
    response_get_one = client_api.get('/api/logs', params={'api_token': '1'})

    assert response_get_null.status_code == 404
    response_json = response_get_one.json()
    assert response_get_one.status_code == 200 and response_json.code == 123 and response_json.message == 'm'\
           and response_json.additioanl == 'a'

    os.remove(f'''../../tests/test_api/logs/{get_hash_email('test@example.com')}.json''')

