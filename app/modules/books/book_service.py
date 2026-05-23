from app.modules.books.book_repository import get_books
from app.helper.helpers import check_author

def get_author_books(author_id: str):
    response = {
        "success": True,
        "code": 200,
        "message": "",
        "data": {},
        "error": None
    }

    is_author_exists = check_author(author_id)
    if not is_author_exists:
        response['message'] = "Unautherized Access"
        response['code'] = 401
        response['success'] = False
        return response
    
    res = get_books(author_id)

    response["message"] = "Successfully get data."
    response['data'] = res
    return response