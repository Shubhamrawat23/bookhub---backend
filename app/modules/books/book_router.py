from fastapi import APIRouter, Query
from app.modules.books.book_service import get_author_books

book_router = APIRouter()

@book_router.get("/book/list")
def author_book_route(author_id:str = Query(...)):
    response = get_author_books(author_id)

    return response