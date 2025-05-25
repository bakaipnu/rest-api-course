from fastapi import APIRouter
from .books import router as books_router


router = APIRouter(prefix="/api")
router.include_router(books_router, prefix="/books")
