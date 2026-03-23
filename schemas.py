from flask_marshmallow import Marshmallow
from models import Article

ma = Marshmallow()

class ArticleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Article
        load_instance = True

article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)