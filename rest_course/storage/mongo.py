import os
from typing import List

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from ..models.book import Book, BookCreate


MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_DB = os.getenv("MONGO_DB")

client = AsyncIOMotorClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}")
db = client[MONGO_DB]
collection = db["books"]


def serialize_book(book) -> Book:
    return Book(
        id=str(book["_id"]),
        title=book["title"],
        author=book["author"]
    )


async def get_all_books() -> List[Book]:
    books_cursor = collection.find()
    books = await books_cursor.to_list(length=100)
    return [serialize_book(b) for b in books]


async def get_book_by_id(book_id: str) -> Book | None:
    book = await collection.find_one({"_id": ObjectId(book_id)})
    if book:
        return serialize_book(book)
    return None


async def add_book(data: BookCreate) -> Book:
    result = await collection.insert_one(data.model_dump())
    new_book = await collection.find_one({"_id": result.inserted_id})
    return serialize_book(new_book)


async def delete_book(book_id: str) -> bool:
    result = await collection.delete_one({"_id": ObjectId(book_id)})
    return result.deleted_count == 1
