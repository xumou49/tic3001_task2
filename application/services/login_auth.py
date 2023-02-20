import bcrypt
from application.models.login import Login
from application.models.user import User


def validate_login(username, password):
    if login_user := Login.objects(username__iexact=username).first():
        if bcrypt.checkpw(password.encode(), login_user.password.encode()):
            return login_user
    return None


def generate_fake_users():
    return [User(**dict(name="Alice", age=21, birthday='2003-01-01', email='alice@gmail.com',
                        university='NUS', address="Street 01", postcode="111111")).save(),
            User(**dict(name="Bob", age=22, birthday='2002-02-02', email='bob@gmail.com',
                        university='NUS', address="Street 02", postcode="222222")).save(),
            User(**dict(name="Clara", age=23, birthday='2001-03-03', email='clara@gmail.com',
                        university='NUS', address="Street 03", postcode="222222")).save()]


def generate_predefined_login_creds():
    users = generate_fake_users()
    Login(**dict(username="alice@gmail.com",
                 password="123456", role="Admin",
                 user=users[0])).save()
    Login(**dict(username="bob@gmail.com",
                 password="123456", role="Editor",
                 user=users[1])).save()
    Login(**dict(username="clara@gmail.com",
                 password="123456", role="Viewer",
                 user=users[2])).save()
