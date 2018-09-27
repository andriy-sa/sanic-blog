import os

from . import credentials

DB_HOST = credentials.DB_HOST
DB_USER = credentials.DB_USER
DB_PASSWORD = credentials.DB_PASSWORD
DB_DATABASE = credentials.DB_NAME
DB_ECHO = True
REDIS = {
    'address': (credentials.REDIS_HOST, credentials.REDIS_PORT),
    # 'db': 0,
    # 'password': 'password',
}

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = credentials.DEBUG
HOLIDAYAPI_KEY = credentials.HOLIDAYAPI_KEY
