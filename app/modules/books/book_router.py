from fastapi import APIRouter, Query, Depends
from app.modules.books.book_service import get_author_books
from app.helper.helpers import require_author

book_router = APIRouter()

@book_router.get("/book/list")
def author_book_route(author_id:str = Query(...), current_user = Depends(require_author)):
    # response = get_author_books(author_id)
    response = get_author_books(current_user['id'])

    return response