from fastapi import APIRouter, Form, File, UploadFile, Query, Depends
from app.modules.tickets.tkt_service import create_tkt, tkts_listing, chat_history, save_chat_history, save_admin_actions, tktDetail_for_admin
from app.modules.tickets.tkt_schemas import SaveMessage, TktActions
from app.helper.helpers import check_admin, require_author

tkt_router = APIRouter()

@tkt_router.post("/author/create")
def author_create_tkt_route(
    author_id: str = Form(...),
    book_id: str = Form(...),
    subject: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    file: UploadFile = File(None)
    ):
    
        data = {
            "author_id": author_id,
            "book_id": book_id,
            "subject": subject,
            "description": description,
            "category": category,
        }
        response = create_tkt(data, file)
        return response

@tkt_router.get("/author/list")
def tkts_author_route(current_user: str= Depends(require_author)):
        response = {
            "success": True,
            "code": 200,
            "message": "",
            "data": {},
            "error": None
        }

        # if author_id == "all":
        #     response['success'] = False
        #     response['code'] = 401
        #     response['message'] = "Unautherized Access"
        #     response['error'] = {
        #             "field":"author_id"
        #     }
        #     return response
        
        # response = tkts_listing(author_id)
        return response

@tkt_router.get("/author/tkt_chat")
def tkt_chat_history_author_route(tkt_code: str = Query(...), access_by: str = Query(...), author_id: str = Query(...)):
        response = chat_history(tkt_code, access_by, author_id)

        return response

@tkt_router.post("/author/save_message")
def save_author_chat_history_route(data: SaveMessage):
        response = save_chat_history(data)

        return response



# get tkts list for admins

@tkt_router.get("/admin/list")
def tkts_admin_route(
        author_id: str = Query(...), # send 'all'
        admin_code: str = Query(...),
        status_filter: str = Query(""), 
        category_filter: str = Query(""), 
        priority_filter: str = Query(""), 
        start_date_tz: str = Query(""), 
        end_date_tz: str = Query("")
    ):
        
        response = {
            "success": True,
            "code": 200,
            "message": "",
            "data": {},
            "error": None
        }

        is_admin_exists = check_admin(admin_code)
        if not is_admin_exists:
                response['message'] = "Unautherized Access"
                response['code'] = 401
                response['success'] = False
                return response

        if (author_id.lower()) != "all":
            response['success'] = False
            response['code'] = 401
            response['message'] = "Unautherized Access"
            response['error'] = {
                    "field":"author_id"
            }
            return response
        
        response = tkts_listing(author_id, status_filter, category_filter, priority_filter, start_date_tz, end_date_tz)
        return response


# get chat history for admin
@tkt_router.get("/admin/tkt_chat")
def tkt_chat_history_admin_route(tkt_code: str = Query(...), access_by: str = Query(...),author_id: str = Query(...)):
        
        response = {
            "success": True,
            "code": 200,
            "message": "",
            "data": {},
            "error": None
        }

        if (access_by.lower()) != "admin":
            response['success'] = False
            response['code'] = 401
            response['message'] = "Unautherized Access"
            response['error'] = {
                    "field":"access_by"
            }
            return response
        
        response = chat_history(tkt_code, access_by, author_id)
        return response


# save admin chat
@tkt_router.post("/admin/save_message")
def save_admin_chat_history_route(data: SaveMessage):
        print(data)
        response = save_chat_history(data)

        return response

# save admin actions

@tkt_router.put("/admin/tkt_action")
def admin_actions_route(data: TktActions):
       resposne = save_admin_actions(data)
       return resposne

# get tkt data for admin
@tkt_router.get('/admin/tkt_detail')
def tktDetail_for_admin_route(admin_code: str, ticket_code:str):
       response = tktDetail_for_admin(admin_code, ticket_code)
       return response