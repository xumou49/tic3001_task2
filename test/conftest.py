from urllib3.util import parse_url
from pathlib import Path
import pytest

from application.models import User

TEST_DIR = Path(__file__).parent


@pytest.fixture(name='_test_app', scope="session")
def test_app():
    from application.app import init_app
    from config import TestConfig
    app, db = init_app(TestConfig)
    ctx = app.app_context()
    ctx.push()

    yield app
    db_name = parse_url(app.config['MONGODB_HOST']).path[1:]
    db.connection.drop_database(db_name)


@pytest.fixture(name='_test_client')
def test_client(_test_app):
    client = _test_app.test_client()
    yield client


@pytest.fixture(name='_temp_user_token')
def temp_user_token(_test_client):
    return create_test_token(_test_client)


def create_test_token(_test_client):
    variables = {
        "username": "alice@gmail.com",
        "password": "123456"
    }
    res = _test_client.post('/api/login-auth/login', json=variables)
    token = res.json['access_token']
    return token


def client_auth_header(token):
    headers = dict()
    headers['Authorization'] = 'Bearer {}'.format(token)
    headers['Accept'] = 'application/json'
    headers['Content-Type'] = 'application/json'

    return headers


@pytest.fixture(name='_temp_user_list')
def temp_user_list(_test_app):
    u1 = User(**dict(name="Alice",
                     age=20,
                     email="Alice@gmail.com",
                     birthday="1990-01-01",
                     university="NUS",
                     address="street 0",
                     postcode="100000")).save()
    u2 = User(**dict(name="Bob",
                     age=21,
                     email="Bob@gmail.com",
                     birthday="1991-01-01",
                     university="NUS",
                     address="street 1",
                     postcode="100001")).save()
    u3 = User(**dict(name="Clara",
                     age=22,
                     email="Clara@gmail.com",
                     birthday="1992-01-01",
                     university="NUS",
                     address="street 2",
                     postcode="100002")).save()
    u4 = User(**dict(name="David",
                     age=23,
                     email="David@gmail.com",
                     birthday="1990-01-01",
                     university="NUS",
                     address="street 3",
                     postcode="100003")).save()
    u5 = User(**dict(name="Edward",
                     age=24,
                     email="Edward@gmail.com",
                     birthday="1990-01-01",
                     university="NUS",
                     address="street 4",
                     postcode="100004")).save()
    users = [u1, u2, u3, u4, u5]
    yield users
    _ = [u.delete() for u in users]
