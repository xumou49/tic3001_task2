from application.models.base import BaseDocument
from mongoengine import StringField, DateField, IntField


class User(BaseDocument):
    name = StringField(required=True)
    age = IntField(required=True)
    email = StringField(required=True)
    birthday = DateField(required=True)
    university = StringField(required=True)
    address = StringField(required=True)
    postcode = StringField(required=True)


if __name__ == "__main__":
    from mongoengine import connect
    connect(host='mongodb://localhost:27017/task2xbw?serverSelectionTimeoutMs=500')
    # u = User(**dict(name="Test", age=21, email="abc@zxc.com")).save()
    # u = User.modify(id="63da5d643fb26daa68d2ab7c", **dict(name="Test1"))
    # print(u)
