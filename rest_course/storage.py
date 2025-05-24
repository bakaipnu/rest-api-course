from typing import List

from .models import Book


_books: List[Book] = []
_next_id = 1


def get_all_books() -> List[Book]:
    return _books


def get_book_by_id(book_id: int) -> Book | None:
    return next((book for book in _books if book["id"] == book_id), None)


def add_book(data: dict) -> Book:
    global _next_id
    book = {"id": _next_id, **data}
    _next_id += 1
    _books.append(book)
    return book


def delete_book(book_id: int) -> bool:
    global _books
    before = len(_books)
    _books = [b for b in _books if b["id"] != book_id]
    return len(_books) < before
