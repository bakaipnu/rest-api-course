from pydantic import BaseModel


class Book(BaseModel):
    id: str
    title: str
    author: str


class BookCreate(BaseModel):
    title: str
    author: str
