from flask import jsonify
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException


def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        response = {
            "error": {
                "code": e.code,
                "name": e.name,
                "description": e.description,
            }
        }
        return jsonify(response), e.code

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return jsonify({"errors": e.messages}), 400

    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        return jsonify({
            "error": {
                "code": 500,
                "name": "Internal Server Error",
                "description": "An unexpected error occurred.",
            }
        }), 500
