from typing import List

from fastapi import APIRouter, HTTPException

from ..models.book import Book, BookCreate
from ..storage.mongo import get_all_books, get_book_by_id, add_book, delete_book


router = APIRouter()


@router.get("/", response_model=List[Book])
async def list_books():
    return await get_all_books()


@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: str):
    book = await get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("/", response_model=Book, status_code=201)
async def create_book(book_data: BookCreate):
    return await add_book(book_data)


@router.delete("/{book_id}", status_code=204)
async def remove_book(book_id: str):
    if not await delete_book(book_id):
        raise HTTPException(status_code=404, detail="Book not found")
