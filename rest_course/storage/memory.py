from typing import List

from ..models.book import Book, BookCreate


_books: List[Book] = []
_next_id = 1


async def get_all_books() -> List[Book]:
    return _books


async def get_book_by_id(book_id: int) -> Book | None:
    return next((book for book in _books if book.id == book_id), None)


async def add_book(data: BookCreate) -> Book:
    global _next_id
    book = Book(id=_next_id, **data.model_dump())
    _next_id += 1
    _books.append(book)
    return book


async def delete_book(book_id: int) -> bool:
    global _books
    before = len(_books)
    _books = [b for b in _books if b.id != book_id]
    return len(_books) < before
