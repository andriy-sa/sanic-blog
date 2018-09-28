from aioelasticsearch import Elasticsearch
from app import db
from config import config
from elastic_docs.article import ArticleDoc
from libraries.helpers import jsonify, model_dict
from libraries.validation import Validation
from models.article import Article
from models.comment import Comment
from sanic import Blueprint
from sanic.response import json
from sqlalchemy import case, desc, func, join, or_

blog = Blueprint('blog')


@blog.route("/")
async def articles_list(request):
    q = request.args.get('q')
    page = int(request.args.get('page')) if request.args.get('page') and request.args.get('page').isdigit() else 1
    limit = int(request.args.get('limit')) if request.args.get('limit') and request.args.get('limit').isdigit() else 10
    offset = limit * (page - 1)

    articles = db.select([Article,
                          case([(Article.is_published == True, func.count(Comment.id))], else_=None).label(
                              'comments_count')]) \
        .select_from(join(Article, Comment, Comment.article_id == Article.id, isouter=True)) \
        .group_by(Article.id)

    if q:
        articles = articles.where(
            or_(Article.title.ilike("%{}%".format(q)), Article.description.ilike("%{}%".format(q))))

    articles = await articles.order_by(desc(Article.created_at)).limit(limit).offset(offset).gino.all()
    return json({'posts': jsonify(articles)})


@blog.route("/autocomplete")
async def articles_list(request):
    q = request.args.get('q')
    limit = int(request.args.get('limit')) if request.args.get('limit') and request.args.get('limit').isdigit() else 10

    query = ArticleDoc.search().filter('term', is_published=True)
    if q:
        query = query.query('match_phrase', title={'query': q, 'analyzer': 'standard'})

    query = query.sort('_score', '-created_at')[0:limit].to_dict()

    async with Elasticsearch([config.ELASTICSEARCH_HOST]) as es:
        result = await es.search(index=ArticleDoc._index._name, body=query)

    return json(result)


@blog.route("/create", methods=['POST'])
async def article_create(request):
    validator = Validation()
    rules = {
        'title': 'required|min:3',
        'is_published': 'required|boolean'
    }
    if not validator.is_valid(request.json or {}, rules):
        return json({'errors': validator.errors}, 400)

    article = await Article.create(**{'title': request.json.get('title'),
                                      'description': request.json.get('description'),
                                      'is_published': request.json.get('is_published')
                                      })

    return json(model_dict(article), 201)


@blog.route("/<id:int>")
async def article_detail(request, id):
    article = await Article.query.where(Article.id == id).gino.first()
    if not article:
        return json({'message': 'Not Found'}, 404)

    return json(model_dict(article))


@blog.route("/update/<id:int>", methods=['PUT'])
async def article_update(request, id):
    article = await Article.query.where(Article.id == id).gino.first()
    if not article:
        return json({'message': 'Not Found'}, 404)

    validator = Validation()
    rules = {
        'title': 'required|min:3',
        'is_published': 'required|boolean'
    }
    if not validator.is_valid(request.json or {}, rules):
        return json({'errors': validator.errors}, 400)

    await article.update(**{
        'title': request.json.get('title'),
        'description': request.json.get('description'),
        'is_published': request.json.get('is_published')
    }).apply()

    return json(model_dict(article))


@blog.route("/delete/<id:int>", methods=['DELETE'])
async def article_delete(request, id):
    article = await Article.query.where(Article.id == id).gino.first()
    if not article:
        return json({'message': 'Not Found'}, 404)

    await article.delete()

    return json(None, 204)
