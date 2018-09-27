import socketio
from config import config
from gino.ext.sanic import Gino
from sanic import Sanic

sio = socketio.AsyncServer(async_mode='sanic')
app = Sanic()
sio.attach(app, socketio_path='/ws')
app.config.from_object(config)
db = Gino()
db.init_app(app)


def create_app():
    from views.blog import blog
    from views.custom import custom
    from views.chat import chat

    app.blueprint(blog, url_prefix='/blog')
    app.blueprint(chat, url_prefix='/chat')
    app.blueprint(custom, url_prefix='/custom')

    return app
