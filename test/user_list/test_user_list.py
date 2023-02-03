import json

import pytest

from application.models import User
from bson import ObjectId


def get_end_point(postfix=""):
    return f'/api/user-list/users{postfix}'


def test_get_users(_test_client, _temp_user_list):
    response = _test_client.get(get_end_point())
    assert response.status_code == 200
    assert response.json == {'users': [{'address': 'street 0',
                                        'age': 20,
                                        'birthday': 'Mon, 01 Jan 1990 00:00:00 GMT',
                                        'email': 'Alice@gmail.com',
                                        'id': str(User.objects(age=20).first().id),
                                        'name': 'Alice',
                                        'postcode': '100000',
                                        'university': 'NUS'},
                                       {'address': 'street 1',
                                        'age': 21,
                                        'birthday': 'Tue, 01 Jan 1991 00:00:00 GMT',
                                        'email': 'Bob@gmail.com',
                                        'id': str(User.objects(age=21).first().id),
                                        'name': 'Bob',
                                        'postcode': '100001',
                                        'university': 'NUS'},
                                       {'address': 'street 2',
                                        'age': 22,
                                        'birthday': 'Wed, 01 Jan 1992 00:00:00 GMT',
                                        'email': 'Clara@gmail.com',
                                        'id': str(User.objects(age=22).first().id),
                                        'name': 'Clara',
                                        'postcode': '100002',
                                        'university': 'NUS'},
                                       {'address': 'street 3',
                                        'age': 23,
                                        'birthday': 'Mon, 01 Jan 1990 00:00:00 GMT',
                                        'email': 'David@gmail.com',
                                        'id': str(User.objects(age=23).first().id),
                                        'name': 'David',
                                        'postcode': '100003',
                                        'university': 'NUS'},
                                       {'address': 'street 4',
                                        'age': 24,
                                        'birthday': 'Mon, 01 Jan 1990 00:00:00 GMT',
                                        'email': 'Edward@gmail.com',
                                        'id': str(User.objects(age=24).first().id),
                                        'name': 'Edward',
                                        'postcode': '100004',
                                        'university': 'NUS'}]}


get_user_cases = [
    (True, lambda v: {'users': {'address': 'street 0',
                                'age': 20,
                                'birthday': 'Mon, 01 Jan 1990 00:00:00 GMT',
                                'email': 'Alice@gmail.com',
                                'id': v,
                                'name': 'Alice',
                                'postcode': '100000',
                                'university': 'NUS'}}),
    (False, lambda v: {'error_message': 'User not found'})
]


@pytest.mark.parametrize("user_exists, expected", get_user_cases)
def test_get_user(_test_client, _temp_user_list, user_exists, expected):
    uid = str(User.objects(age=20).first().id) if user_exists else str(ObjectId())
    response = _test_client.get(get_end_point(f'/{uid}'))
    assert response.status_code == 200 if user_exists else 404
    assert response.json == expected(uid)


create_user_cases = [
    ({"address": "street 0", "age": 20, "birthday": "2021-01-01",
      "email": "Alice@gmail.com", "name": "Alice", "postcode": "987654", "university": "NUS"},
     lambda v: {'users': {'address': 'street 0', 'age': 20, 'birthday': '2021-01-01', 'email': 'Alice@gmail.com',
                          'id': v, 'name': 'Alice', 'postcode': '987654', 'university': 'NUS'}}),
    ({"address": "street 1", "age": 2000, "birthday": "2021-01-01",
      "email": "Alice@gmail.com", "name": "Alice", "postcode": "100000", "university": "NUS"},
     lambda v: {'error_message': 'Invalid age'}),
    ({"address": "street 2", "age": 20, "birthday": "2021-JAN-01",
      "email": "Alice@gmail.com", "name": "Alice", "postcode": "100000", "university": "NUS"},
     lambda v: {'error_message': 'Invalid birthday format, example format: 2000-01-01'}),
    ({"address": "street 2", "age": 20, "birthday": "2021-01-01",
      "email": "Alice#gmail.com", "name": "Alice", "postcode": "100000", "university": "NUS"},
     lambda v: {'error_message': 'Invalid email address'}),
    ({"address": "street 2", "age": 20, "birthday": "2021-01-01",
      "email": "Alice@gmail.com", "name": "Alice", "postcode": "1000001", "university": "NUS"},
     lambda v: {'error_message': 'Invalid postcode, it should be in 6 digit number'}),
]


@pytest.mark.parametrize("user, expected", create_user_cases)
def test_create_user(_test_client, user, expected):
    response = _test_client.post(
        get_end_point(), data=json.dumps(user), content_type='application/json')
    assert response.status_code == 201 or 404
    assert response.json == expected(str(User.objects(postcode='987654').first().id))


update_user_cases = [
    (True, {"address": "street 1", "age": 20, "birthday": "2021-01-02",
            "email": "Alice1@gmail.com", "name": "Alice", "postcode": "987653", "university": "NTU"},
     lambda uid: {'users': {'address': 'street 1', 'age': 20, 'birthday': 'Sat, 02 Jan 2021 00:00:00 GMT',
                            'email': 'Alice1@gmail.com', 'id': uid, 'name': 'Alice',
                            'postcode': '987653', 'university': 'NTU'}}),
    (True, {"address": "street 0", "age": 2000, "birthday": "2021-01-01",
            "email": "Alice@gmail.com", "name": "Alice", "postcode": "987654", "university": "NUS"},
     lambda uid: {'error_message': 'Invalid age'}),
    (True, {"address": "street 0", "age": 20, "birthday": "2021-JAN-01",
            "email": "Alice@gmail.com", "name": "Alice", "postcode": "987654", "university": "NUS"},
     lambda uid: {'error_message': 'Invalid birthday format, example format: 2000-01-01'}),
    (True, {"address": "street 0", "age": 20, "birthday": "2021-01-01",
            "email": "Alice@gmail.com", "name": "Alice", "postcode": "1000001", "university": "NUS"},
     lambda uid: {'error_message': 'Invalid postcode, it should be in 6 digit number'}),
    (True, {"address": "street 0", "age": 20, "birthday": "2021-01-01",
            "email": "Alice#gmail.com", "name": "Alice", "postcode": "987654", "university": "NUS"},
     lambda uid: {'error_message': 'Invalid email address'}),
    (False, {"address": "street 0", "age": 20, "birthday": "2021-01-01",
             "email": "Alice@gmail.com", "name": "Alice", "postcode": "987654", "university": "NUS"},
     lambda uid: {'error_message': 'User not found'}),
]


@pytest.mark.parametrize("user_exists, user_updates, expected", update_user_cases)
def test_update_user(_test_client, _temp_user_list, user_exists, user_updates, expected):
    uid = str(User.objects(age=20).first().id) if user_exists else str(ObjectId())
    response = _test_client.put(
        get_end_point(f'/{uid}'), data=json.dumps(user_updates), content_type='application/json')
    assert response.status_code == 200 or 404
    assert response.json == expected(uid)


delete_user_cases = [
    (True, {'users': {'deleted': True}}),
    (False, {'error_message': 'User not found'})
]


@pytest.mark.parametrize("user_exists, expected", delete_user_cases)
def test_delete_user(_test_client, _temp_user_list, user_exists, expected):
    uid = str(User.objects(age=20).first().id) if user_exists else str(ObjectId())
    response = _test_client.delete(get_end_point(f'/{uid}'))
    assert response.status_code == 200 if user_exists else 404
    assert response.json == expected
