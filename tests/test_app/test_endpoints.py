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
def client_app():
    with TestClient(app=app, base_url='http://localhost:1001') as client:
        yield client


@pytest.fixture(scope='function')
def set_override_test_db():
    with DependencyOverrider(
            app, overrides={database.get_db: override_database.get_db}
    ) as overrider:
        yield overrider


def test_routers(client_app, set_override_test_db, db: Session = next(override_database.get_db())):
    db.query(User).delete()
    db.commit()

    user = User(email='test@example.com', hashed_password='secret', api_token='1'
                ).services = Notification(id=)

    db.add(user)
    db.commit()
