from flasgger import Swagger


def register_swagger(app):
    Swagger(app, template={
        "swagger": "2.0",
        "info": {
            "title": "Book API",
            "description": "API for managing books",
            "version": "1.0.0"
        },
        "definitions": {
            "Book": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "title": {"type": "string"},
                    "author": {"type": "string"}
                },
                "required": ["title", "author"]
            }
        }
    })
