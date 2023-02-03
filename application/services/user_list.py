import re
from application.services.exceptions import BackendError


def validate_user(user, is_update=False):
    if not user.get('name', None):
        if not is_update:
            raise BackendError("Name is not defined")
    if not (age := user.get('age', None)):
        if not is_update:
            raise BackendError("Age is not defined")
    if not (email := user.get('email', None)):
        if not is_update:
            raise BackendError("Email is not defined")
    if not (birthday := user.get('birthday', None)):
        if not is_update:
            raise BackendError("Birthday is not defined")
    if not user.get('university', None):
        if not is_update:
            raise BackendError("University is not defined")
    if not user.get('address', None):
        if not is_update:
            raise BackendError('Address', None)
    if not (postcode := user.get('postcode', None)):
        if not is_update:
            raise BackendError("Postcode is not defined")
    if not re.search(r'^\d{1,3}$', str(age)) and age:
        raise BackendError("Invalid age")
    if not re.search(r'^\d{4}-\d{2}-\d{2}$', birthday) and age:
        raise BackendError("Invalid birthday format, example format: 2000-01-01")
    if not re.search(r"^[^@]+@[^.]+\..+$", email) and email:
        raise BackendError("Invalid email address")
    if not re.search(r'^\d{6}$', postcode) and postcode:
        raise BackendError("Invalid postcode, it should be in 6 digit number")


def validate_create_user(user):
    validate_user(user, is_update=False)


def validate_update_user(user):
    validate_user(user, is_update=True)



