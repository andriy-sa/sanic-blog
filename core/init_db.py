from asyncpg import create_pool
from sanic import Blueprint

db_bp = Blueprint('db_bp')


class pg:
    def __init__(self, pg_pool):
        self.pg_pool = pg_pool

    async def fetch(self, sql, *args, **kwargs):
        async with self.pg_pool.acquire() as connection:
            return await connection.fetch(sql, *args, **kwargs)

    async def execute(self, sql, *args, **kwargs):
        async with self.pg_pool.acquire() as connection:
            return await connection.execute(sql, *args, **kwargs)


@db_bp.listener('before_server_start')
async def init_pg(app, loop):
    """
    Init Postgresql DB.
    """
    db_bp.pg_pool = await create_pool(
        host=app.config['DB']['host'],
        user=app.config['DB']['user'],
        password=app.config['DB']['password'],
        database=app.config['DB']['database'],
        min_size=1,
        max_size=3,
        loop=loop,
        max_inactive_connection_lifetime=60,
    )
    app.pg = pg(db_bp.pg_pool)
