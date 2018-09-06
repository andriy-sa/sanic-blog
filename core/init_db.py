from asyncpg import create_pool
from config import config
from core.database import DB
from sanic import Blueprint

db_bp = Blueprint('db_bp')


@db_bp.listener('before_server_start')
async def init_pg(app, loop):
    """
    Init Postgresql DB.
    """
    DB.pool = await create_pool(
        host=config.DB['host'],
        user=config.DB['user'],
        password=config.DB['password'],
        database=config.DB['database'],
        min_size=1,
        max_size=3,
        max_inactive_connection_lifetime=60,
    )
    app.pg = DB
