import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Book


DATABASE_URL = (f"postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@"
                f"{os.getenv("POSTGRES_HOST")}:5432/{os.getenv("POSTGRES_DB")}")


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def get_all_books(limit: int = 10, offset: int = 0) -> list[Book]:
    with SessionLocal() as session:
        return session.query(Book).offset(offset).limit(limit).all()


def get_books_after_cursor(cursor: int | None, limit: int = 10) -> list[Book]:
    with SessionLocal() as session:
        query = session.query(Book).order_by(Book.id)

        if cursor is not None:
            query = query.filter(Book.id > cursor)

        return query.limit(limit).all()


def get_book_by_id(book_id: int) -> Book | None:
    with SessionLocal() as session:
        return session.query(Book).filter(Book.id == book_id).first()


def add_book(book: Book) -> Book:
    with SessionLocal() as session:
        session.add(book)
        session.commit()
        session.refresh(book)
        return book


def delete_book(book_id: int) -> bool:
    with SessionLocal() as session:
        book = session.query(Book).filter(Book.id == book_id).first()
        if book:
            session.delete(book)
            session.commit()
            return True
        return False
