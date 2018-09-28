from elasticsearch_dsl import Boolean, Date, Document, Text, analyzer, token_filter

standard_analyzer = analyzer('standard',
                             tokenizer="standard",
                             filter=["standard", "lowercase"]
                             )

ngram_analyzer = analyzer(
    'ngram_analyzer',
    type='custom',
    tokenizer='standard',
    filter=[
        'lowercase',
        token_filter(
            'ngram_filter', type='ngram',
            min_gram=1, max_gram=80
        )
    ]
)


class ArticleDoc(Document):
    title = Text(analyzer=ngram_analyzer)
    description = Text(analyzer=standard_analyzer)
    is_published = Boolean()
    created_at = Date()

    class Index:
        name = 'sanic_articles'
        settings = {
            "number_of_shards": 5,
            "number_of_replicas": 1,
        }
