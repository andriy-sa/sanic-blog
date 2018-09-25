import os

from . import credentials

DB = {
    'host': credentials.DB_HOST,
    'user': credentials.DB_USER,
    'password': credentials.DB_PASSWORD,
    'database': credentials.DB_NAME
}

REDIS = {
    'address': (credentials.REDIS_HOST, credentials.REDIS_PORT),
    # 'db': 0,
    # 'password': 'password',
}

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = credentials.DEBUG
HOLIDAYAPI_KEY = credentials.HOLIDAYAPI_KEY
