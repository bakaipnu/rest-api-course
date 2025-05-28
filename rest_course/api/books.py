from flask import request
from flask_restful import Resource, abort
from marshmallow import ValidationError
from flasgger.utils import swag_from

from rest_course.schemas import BookSchema
from rest_course.storage import get_books_after_cursor, get_book_by_id, add_book, delete_book


book_schema = BookSchema()
books_schema = BookSchema(many=True)


class BookListResource(Resource):
    @swag_from({
        'tags': ['Books'],
        'parameters': [
            {
                'name': 'cursor',
                'in': 'query',
                'type': 'integer',
                'required': False,
                'description': 'Pagination cursor'
            },
            {
                'name': 'limit',
                'in': 'query',
                'type': 'integer',
                'required': False,
                'default': 10,
                'description': 'Maximum number of books to return'
            }
        ],
        'responses': {
            200: {
                'description': 'A list of books',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'results': {
                            'type': 'array',
                            'items': {'$ref': '#/definitions/Book'}
                        },
                        'next_cursor': {'type': 'integer'}
                    }
                }
            }
        }
    })
    def get(self):
        cursor = request.args.get("cursor", type=int)
        limit = request.args.get("limit", default=10, type=int)
        books = get_books_after_cursor(cursor=cursor, limit=limit)
        next_cursor = books[-1].id if books else None

        return {
            "results": books_schema.dump(books),
            "next_cursor": next_cursor
        }, 200

    @swag_from({
        'tags': ['Books'],
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    '$ref': '#/definitions/Book'
                },
                'examples': {
                    'application/json': {
                        'title': 'Martin Eden',
                        'author': 'Jack London'
                    }
                }
            }
        ],
        'responses': {
            201: {
                'description': 'Book successfully created',
                'schema': {'$ref': '#/definitions/Book'}
            },
            400: {
                'description': 'Validation error'
            }
        }
    })
    def post(self):
        try:
            validated = book_schema.load(request.json)
        except ValidationError as err:
            return {"errors": err.messages}, 400

        book = add_book(validated)
        return book_schema.dump(book), 201


class BookResource(Resource):
    @swag_from({
        'tags': ['Books'],
        'parameters': [
            {
                'name': 'book_id',
                'in': 'path',
                'type': 'integer',
                'required': True,
                'description': 'ID of the book to retrieve'
            }
        ],
        'responses': {
            200: {
                'description': 'Book found',
                'schema': {'$ref': '#/definitions/Book'}
            },
            404: {
                'description': 'Book not found'
            }
        }
    })
    def get(self, book_id):
        book = get_book_by_id(book_id)
        if book is None:
            abort(404, message="Book not found")
        return book_schema.dump(book), 200

    @swag_from({
        'tags': ['Books'],
        'parameters': [
            {
                'name': 'book_id',
                'in': 'path',
                'type': 'integer',
                'required': True,
                'description': 'ID of the book to delete'
            }
        ],
        'responses': {
            204: {
                'description': 'Book deleted'
            },
            404: {
                'description': 'Book not found'
            }
        }
    })
    def delete(self, book_id):
        if delete_book(book_id):
            return '', 204
        else:
            abort(404, message="Book not found")
            return None
