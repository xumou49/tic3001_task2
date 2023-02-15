import os
from datetime import timedelta


class BaseConfig:
    MONGODB_HOST = os.environ.get('MONGODB_HOST', 'mongodb://localhost:27017/task2xbw?serverSelectionTimeoutMs=500')
    # JWT
    JWT_SECRETS = os.environ.get('JWT_SECRETS', 'xbw_assignment_tasks')
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRATION_DELTA = timedelta(hours=1)
    JWT_EXPIRATION = 3600 * 3  # 3 hours
    JWT_EXPIRATION_LONG = 86400 * 30  # 30 days

    ADMIN_CLAIMS = [
        'view:user',
        'edit:user',
        'remove:user',
    ]
    EDITOR_CLAIMS = [
        'view:user',
        'edit:user',
    ]
    VIEWER_CLAIMS = [
        'view:user'
    ]


class TestConfig(BaseConfig):
    MONGODB_HOST = os.environ.get('MONGODB_HOST',
                                  'mongodb://localhost:27017/task2xbw-test?serverSelectionTimeoutMs=5000')
