from . import credentials

DB = {
    'host': credentials.DB_HOST,
    'user': credentials.DB_USER,
    'password': credentials.DB_PASSWORD,
    'database': credentials.DB_NAME
}

DEBUG = credentials.DEBUG
