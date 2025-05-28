from flask import Blueprint
from flask_restful import Api

from rest_course.schemas import BookSchema
from rest_course.api.books import BookListResource, BookResource


bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(bp)
api.add_resource(BookListResource, "/books")
api.add_resource(BookResource, "/books/<int:book_id>")

book_schema = BookSchema()
books_schema = BookSchema(many=True)
