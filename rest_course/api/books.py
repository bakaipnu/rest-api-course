from flask import request
from flask_restful import Resource, abort
from marshmallow import ValidationError

from rest_course.schemas import BookSchema
from rest_course.storage import get_books_after_cursor, get_book_by_id, add_book, delete_book


book_schema = BookSchema()
books_schema = BookSchema(many=True)


class BookListResource(Resource):
    def get(self):
        cursor = request.args.get("cursor", type=int)
        limit = request.args.get("limit", default=10, type=int)
        books = get_books_after_cursor(cursor=cursor, limit=limit)
        next_cursor = books[-1].id if books else None

        return {
            "results": books_schema.dump(books),
            "next_cursor": next_cursor
        }, 200

    def post(self):
        try:
            validated = book_schema.load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        book = add_book(validated)
        return book_schema.dump(book), 201


class BookResource(Resource):
    def get(self, book_id):
        book = get_book_by_id(book_id)
        if book is None:
            abort(404, message="Book not found")
        return book_schema.dump(book), 200

    def delete(self, book_id):
        if delete_book(book_id):
            return '', 204
        else:
            abort(404, message="Book not found")
            return None
