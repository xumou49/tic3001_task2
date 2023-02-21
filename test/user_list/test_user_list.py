import json

import pytest

from application.models import User
from bson import ObjectId

from test.conftest import client_auth_header


def get_end_point(postfix=""):
    return f'/api/user-list/users{postfix}'


def test_get_users(_test_client, _temp_user_token, _temp_user_list):
    response = _test_client.get(get_end_point(), headers=client_auth_header(_temp_user_token))
    assert response.status_code == 200
    assert response.json == {'users': [
        {'address': 'Street 01',
         'age': 21,
         'birthday': '2003-01-01',
         'email': 'alice@gmail.com',
         'id': str(User.objects(postcode='111111').first().id),
         'name': 'Alice',
         'postcode': '111111',
         'university': 'NUS'},
        {'address': 'Street 02',
         'age': 22,
         'birthday': '2002-02-02',
         'email': 'bob@gmail.com',
         'id': str(User.objects(postcode='222222').first().id),
         'name': 'Bob',
         'postcode': '222222',
         'university': 'NUS'},
        {'address': 'Street 03',
         'age': 23,
         'birthday': '2001-03-03',
         'email': 'clara@gmail.com',
         'id': str(User.objects(postcode='333333').first().id),
         'name': 'Clara',
         'postcode': '333333',
         'university': 'NUS'},
        {'address': 'street 0',
         'age': 20,
         'birthday': '1990-01-01',
         'email': 'Alice@gmail.com',
         'id': str(User.objects(postcode='100000').first().id),
         'name': 'Alice',
         'postcode': '100000',
         'university': 'NUS'},
        {'address': 'street 1',
         'age': 21,
         'birthday': '1991-01-01',
         'email': 'Bob@gmail.com',
         'id': str(User.objects(postcode='100001').first().id),
         'name': 'Bob',
         'postcode': '100001',
         'university': 'NUS'},
        {'address': 'street 2',
         'age': 22,
         'birthday': '1992-01-01',
         'email': 'Clara@gmail.com',
         'id': str(User.objects(postcode='100002').first().id),
         'name': 'Clara',
         'postcode': '100002',
         'university': 'NUS'},
        {'address': 'street 3',
         'age': 23,
         'birthday': '1990-01-01',
         'email': 'David@gmail.com',
         'id': str(User.objects(postcode='100003').first().id),
         'name': 'David',
         'postcode': '100003',
         'university': 'NUS'},
        {'address': 'street 4',
         'age': 24,
         'birthday': '1990-01-01',
         'email': 'Edward@gmail.com',
         'id': str(User.objects(postcode='100004').first().id),
         'name': 'Edward',
         'postcode': '100004',
         'university': 'NUS'}]}


get_user_cases = [
    (True, lambda v: {'users': {'address': 'street 0',
                                'age': 20,
                                'birthday': '1990-01-01',
                                'email': 'Alice@gmail.com',
                                'id': v,
                                'name': 'Alice',
                                'postcode': '100000',
                                'university': 'NUS'}}),
    (False, lambda v: {'error_message': 'User not found'})
]


@pytest.mark.parametrize("user_exists, expected", get_user_cases)
def test_get_user(_test_client, _temp_user_token, _temp_user_list, user_exists, expected):
    uid = str(User.objects(age=20).first().id) if user_exists else str(ObjectId())
    response = _test_client.get(get_end_point(f'/{uid}'), headers=client_auth_header(_temp_user_token))
    assert response.status_code == 200 if user_exists else 404
    assert response.json == expected(uid)


create_user_cases = [
    ({"address": "street 0", "age": 20, "birthday": "2021-01-01",
      "email": "Alice0@gmail.com", "name": "Alice", "postcode": "987654", "university": "NUS"},
     lambda v: {'users': {'address': 'street 0', 'age': 20, 'birthday': '2021-01-01', 'email': 'Alice0@gmail.com',
                          'id': v, 'name': 'Alice', 'postcode': '987654', 'university': 'NUS'}}),
    ({"address": "street 1", "age": 2000, "birthday": "2021-01-01",
      "email": "Alice1@gmail.com", "name": "Alice", "postcode": "100000", "university": "NUS"},
     lambda v: {'error_message': 'Invalid age'}),
    ({"address": "street 2", "age": 20, "birthday": "2021-JAN-01",
      "email": "Alice2@gmail.com", "name": "Alice", "postcode": "100000", "university": "NUS"},
     lambda v: {'error_message': 'Invalid birthday format, example format: 2000-01-01'}),
    ({"address": "street 2", "age": 20, "birthday": "2021-01-01",
      "email": "Alice#gmail.com", "name": "Alice", "postcode": "100000", "university": "NUS"},
     lambda v: {'error_message': 'Invalid email address'}),
    ({"address": "street 2", "age": 20, "birthday": "2021-01-01",
      "email": "Alice3@gmail.com", "name": "Alice", "postcode": "10000000001", "university": "NUS"},
     lambda v: {'error_message': 'Invalid postcode, it should be between 3-10 digit number'}),
]


@pytest.mark.parametrize("user, expected", create_user_cases)
def test_create_user(_test_client, _temp_user_token, user, expected):
    response = _test_client.post(
        get_end_point(), data=json.dumps(user), headers=client_auth_header(_temp_user_token))
    assert response.status_code == 201 or 404
    assert response.json == expected(str(User.objects(postcode='987654').first().id))


update_user_cases = [
    (True, {"address": "street 1", "age": 20, "birthday": "2021-01-02",
            "email": "Alice1@gmail.com", "name": "Alice", "postcode": "987653", "university": "NTU"},
     lambda uid: {'users': {'address': 'street 1', 'age': 20, 'birthday': '2021-01-02',
                            'email': 'Alice1@gmail.com', 'id': uid, 'name': 'Alice',
                            'postcode': '987653', 'university': 'NTU'}}),
    (True, {"address": "street 0", "age": 2000, "birthday": "2021-01-01",
            "email": "Alice@gmail.com", "name": "Alice", "postcode": "987654", "university": "NUS"},
     lambda uid: {'error_message': 'Invalid age'}),
    (True, {"address": "street 0", "age": 20, "birthday": "2021-JAN-01",
            "email": "Alice@gmail.com", "name": "Alice", "postcode": "987654", "university": "NUS"},
     lambda uid: {'error_message': 'Invalid birthday format, example format: 2000-01-01'}),
    (True, {"address": "street 0", "age": 20, "birthday": "2021-01-01",
            "email": "Alice@gmail.com", "name": "Alice", "postcode": "100000000001", "university": "NUS"},
     lambda uid: {'error_message': 'Invalid postcode, it should be between 3-10 digit number'}),
    (True, {"address": "street 0", "age": 20, "birthday": "2021-01-01",
            "email": "Alice#gmail.com", "name": "Alice", "postcode": "987654", "university": "NUS"},
     lambda uid: {'error_message': 'Invalid email address'}),
    (False, {"address": "street 0", "age": 20, "birthday": "2021-01-01",
             "email": "Alice@gmail.com", "name": "Alice", "postcode": "987654", "university": "NUS"},
     lambda uid: {'error_message': 'User not found'}),
]


@pytest.mark.parametrize("user_exists, user_updates, expected", update_user_cases)
def test_update_user(_test_client, _temp_user_token, _temp_user_list, user_exists, user_updates, expected):
    uid = str(User.objects(age=20).first().id) if user_exists else str(ObjectId())
    response = _test_client.put(
        get_end_point(f'/{uid}'), data=json.dumps(user_updates), headers=client_auth_header(_temp_user_token))
    assert response.status_code == 200 or 404
    assert response.json == expected(uid)


delete_user_cases = [
    (True, {'users': {'deleted': True}}),
    (False, {'error_message': 'User not found'})
]


@pytest.mark.parametrize("user_exists, expected", delete_user_cases)
def test_delete_user(_test_client, _temp_user_token, _temp_user_list, user_exists, expected):
    uid = str(User.objects(age=20).first().id) if user_exists else str(ObjectId())
    response = _test_client.delete(get_end_point(f'/{uid}'), headers=client_auth_header(_temp_user_token))
    assert response.status_code == 200 if user_exists else 404
    assert response.json == expected
