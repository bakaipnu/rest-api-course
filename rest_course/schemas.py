from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from rest_course.models import db, Book


class BookSchema(SQLAlchemySchema):
    class Meta:
        model = Book
        load_instance = True
        sqla_session = db.session

    id = auto_field()
    title = auto_field()
    author = auto_field()
