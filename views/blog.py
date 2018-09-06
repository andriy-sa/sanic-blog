from core.database import DB
from libraries.helpers import jsonify
from models.article import Article
from sanic import Blueprint
from sanic.response import json

blog = Blueprint('blog')


@blog.route("/")
async def test(request):
    results = await DB.select([Article]).execute()
    print(results)
    return json({'posts': jsonify(results)})
