from enum import Enum
import bcrypt
import importlib
from application.models.base import BaseDocument
from mongoengine import StringField, ReferenceField, CASCADE
from flask_login import UserMixin


def import_reference_class(module_name):
    return importlib.import_module(module_name)


class Login(BaseDocument, UserMixin):
    class Role(Enum):
        ADMIN = 'Admin'
        VIEWER = 'Viewer'
        EDITOR = 'Editor'

    import_reference_class('application.models.user')
    username = StringField(required=True)
    password = StringField(required=True)
    role = StringField(default=[Role.VIEWER.value])
    user = ReferenceField('User', required=True, reverse_delete_rule=CASCADE)

    def validate(self, clean=True):
        # hash the password if user is newly created or password gets changed
        if self._created or 'password' in self._get_changed_fields():
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(self.password.encode(), salt)
            self.password = hashed.decode('utf-8')
        return super().validate(clean)


if __name__ == "__main__":
    from mongoengine import connect
    connect(host='mongodb://localhost:27017/task2xbw?serverSelectionTimeoutMs=500')
    Login(**{
        "username": "Alice@gmail.com",
        "password": "123456",
        "role":"Admin",
        "user": "63dc6d7bece25609ce3d44ed"
    }).save()
