from flask import Blueprint, jsonify, request, abort
from marshmallow import ValidationError

from .schemas import BookSchema
from .storage import get_books_after_cursor, get_book_by_id, add_book, delete_book


bp = Blueprint("api", __name__, url_prefix="/api")
book_schema = BookSchema()
books_schema = BookSchema(many=True)


@bp.route("/books", methods=["GET"])
def list_books():
    cursor = request.args.get("cursor", type=int)
    limit = request.args.get("limit", default=10, type=int)

    books = get_books_after_cursor(cursor=cursor, limit=limit)

    next_cursor = books[-1].id if books else None

    return jsonify({
        "results": books_schema.dump(books),
        "next_cursor": next_cursor
    }), 200


@bp.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = get_book_by_id(book_id)
    if book is None:
        abort(404, description="Book not found")
    return jsonify(book_schema.dump(book)), 200


@bp.route("/books", methods=["POST"])
def create_book():
    try:
        validated = book_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    book = add_book(validated)
    return jsonify(book_schema.dump(book)), 201


@bp.route("/books/<int:book_id>", methods=["DELETE"])
def remove_book(book_id):
    if delete_book(book_id):
        return "", 204
    else:
        abort(404, description="Book not found")
