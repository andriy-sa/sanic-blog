from core.database import DB
from libraries.helpers import jsonify
from libraries.validation import Validation
from models.article import Article
from sanic import Blueprint
from sanic.response import json
from sqlalchemy import desc, or_

blog = Blueprint('blog')


@blog.route("/")
async def articles_list(request):
    q = request.args.get('q')
    page = int(request.args.get('page')) if request.args.get('page') and request.args.get('page').isdigit() else 1
    limit = int(request.args.get('limit')) if request.args.get('limit') and request.args.get('limit').isdigit() else 10
    offset = limit * (page - 1)

    results = DB.select([Article]).where(Article.is_published == True)

    if q:
        results = results.where(or_(Article.title.ilike("%{}%".format(q)), Article.description.ilike("%{}%".format(q))))

    results = await results.order_by(desc(Article.created_at)).limit(limit).offset(offset).execute()

    return json({'posts': jsonify(results)})


@blog.route("/create", methods=['POST'])
async def article_create(request):
    validator = Validation()
    rules = {
        'title': 'required|min:3',
        'is_published': 'required|boolean'
    }
    if not validator.is_valid(request.json or {}, rules):
        return json({'errors': validator.errors}, 400)

    article = await DB.insert(Article.__table__).values({
        'title': request.json.get('title'),
        'description': request.json.get('description'),
        'is_published': request.json.get('is_published')
    }).execute()

    return json(jsonify(article)[0])


@blog.route("/<id:int>")
async def article_detail(request, id):
    article = await DB.select([Article]).where(Article.is_published == True).where(Article.id == id).execute()
    if not len(article):
        return json({'message': 'Not Found'}, 404)
    return json(jsonify(article)[0])


@blog.route("/update/<id:int>", methods=['PUT'])
async def article_update(request, id):
    article = await DB.select([Article]).where(Article.id == id).execute()
    if not len(article):
        return json({'message': 'Not Found'}, 404)

    validator = Validation()
    rules = {
        'title': 'required|min:3',
        'is_published': 'required|boolean'
    }
    if not validator.is_valid(request.json or {}, rules):
        return json({'errors': validator.errors}, 400)

    article = await DB.update(Article.__table__).where(Article.id == id).values({
        'title': request.json.get('title'),
        'description': request.json.get('description'),
        'is_published': request.json.get('is_published')
    }).execute()

    return json(jsonify(article)[0])


@blog.route("/delete/<id:int>", methods=['DELETE'])
async def article_delete(request, id):
    article = await DB.select([Article]).where(Article.id == id).execute()
    if not len(article):
        return json({'message': 'Not Found'}, 404)

    await DB.delete(Article.__table__).where(Article.id == id).execute()

    return json(None, 204)
