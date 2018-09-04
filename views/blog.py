from app import app
from libraries.helpers import jsonify
from sanic import Blueprint
from sanic.response import json

blog = Blueprint('blog')


@blog.route("/")
async def test(request):
    results = await app.pg.fetch('SELECT * FROM articles')
    return json({'posts': jsonify(results)})
