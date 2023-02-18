import os


class BaseConfig:
    MONGODB_HOST = os.environ.get('MONGODB_HOST', 'mongodb://localhost:27017/task2xbw?serverSelectionTimeoutMs=5000')


class TestConfig(BaseConfig):
    MONGODB_HOST = os.environ.get('MONGODB_HOST',
                                  'mongodb://localhost:27017/task2xbw-test?serverSelectionTimeoutMs=5000')
