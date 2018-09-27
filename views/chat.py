from urllib.parse import parse_qs, urlparse

import aioredis
from aioredis.pubsub import Receiver
from app import app, sio
from sanic import Blueprint
from sanic.response import file
from websockets.exceptions import ConnectionClosed

chat = Blueprint('chat')
users = []


async def redis_listener():
    redis = await aioredis.create_redis('redis://redishost:6379')
    receiver = Receiver()
    await redis.subscribe(receiver.channel('sockets:notification:message'),
                          receiver.channel('sockets:notification:message2'))

    while await receiver.wait_message():
        sender, msg = await receiver.get()
        for sid in users:
            await sio.emit('notification:message', {'data': str(msg)}, room=sid)


@app.listener('before_server_start')
async def before_server_start(sanic, loop):
    sio.start_background_task(redis_listener)


@chat.route("/test")
async def chat_test(request):
    return await file("{}/templates/{}".format(app.config['ROOT_DIR'], 'test.html'))


@sio.on('connect')
async def test_connect(sid, environ):
    pass


@sio.on('on_connected')
async def on_connected(sid, message):
    users.append(sid)


def disconnect_user(sid):
    if sid in users:
        users.remove(sid)


@sio.on('disconnect')
def test_disconnect(sid):
    disconnect_user(sid)


@chat.exception(ConnectionClosed)
async def ignore_404s(request, exception):
    query = parse_qs(urlparse(request.url).query)
    if 'sid' in query:
        sid = query['sid'][0] if isinstance(query['sid'], list) else query['sid']
        disconnect_user(sid)
