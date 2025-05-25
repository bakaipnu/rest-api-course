from flask import Flask

from .errors import register_error_handlers
from .views import bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)
    register_error_handlers(app)
    return app
