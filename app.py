from config import config
from core.init_db import db_bp
from sanic import Sanic

app = Sanic()
app.blueprint(db_bp)
app.config.from_object(config)


def create_app():
    from views.blog import blog
    app.blueprint(blog, url_prefix='/blog')

    return app
