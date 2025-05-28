import os

from flask import Flask
from flask_migrate import Migrate

from .errors import register_error_handlers
from .models import db
from .schemas import BookSwaggerSchema
from .swagger_config import register_swagger
from .views import bp


migrate = Migrate()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    migrate.init_app(app, db)

    app.register_blueprint(bp)
    register_error_handlers(app)

    register_swagger(app)

    return app
