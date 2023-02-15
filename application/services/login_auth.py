import bcrypt
from application.models.login import Login


def validate_login(username, password):
    if login_user := Login.objects(username=username).first():
        if bcrypt.checkpw(password.encode(), login_user.password.encode()):
            return login_user
    return None