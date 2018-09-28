import click
import psycopg2
from elasticsearch_dsl import connections

from config import config
from elastic_docs.article import ArticleDoc


@click.group()
def cli():
    pass


@cli.command()
def index_create():
    # establish connection to elasticseatch
    connections.create_connection(hosts=[config.ELASTICSEARCH_HOST], timeout=20)

    if ArticleDoc._index.exists():
        ArticleDoc._index.delete()
    ArticleDoc.init()
    click.echo('Index was successfully created!')


@cli.command()
def sync_posts():
    # establish connection to postgres
    conn = psycopg2.connect(
        "dbname='{}' user='{}' host='{}' password='{}'".format(config.DB_DATABASE, config.DB_USER,
                                                               config.DB_HOST, config.DB_PASSWORD))

    # establish connection to elasticseatch
    connections.create_connection(hosts=[config.ELASTICSEARCH_HOST], timeout=20)

    cur = conn.cursor()
    cur.execute("""SELECT * from articles""")

    columns = [desc[0] for desc in cur.description]
    rows = cur.fetchall()

    for article in rows:
        article = {key: value for key, value in zip(columns, article)}

        document = ArticleDoc.get(str(article['id']), ignore=404)
        if not document:
            document = ArticleDoc()
        document.meta.id = str(article['id'])
        document.title = article['title']
        document.description = article['description']
        document.is_published = article['is_published']
        document.created_at = article['created_at']
        document.save()

    click.echo('Posts were successfully synced to ElasticSearch!')


if __name__ == '__main__':
    cli()
