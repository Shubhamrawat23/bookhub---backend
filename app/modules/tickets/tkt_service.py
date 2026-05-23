from app.modules.tickets.tkt_repository import check_tkt_existed, entry_in_query_tkts, save_converstion, fetch_authors_tkt, get_chat_history, save_chat, save_action_for_tkt, fetch_tkt_data_for_admin
from app.helper.helpers import check_author, check_admin
import os, re


# author create tkts
def create_tkt(data, file):
    response = {
        "success": True,
        "code": 200,
        "message": "",
        "data": {},
        "error": None
    }

    is_author_exists = check_author(data['author_id'])
    if not is_author_exists:
        response['message'] = "Unautherized Access"
        response['code'] = 401
        response['success'] = False
        return response

    required_fields = ['author_id', 'book_id', 'subject', 'description']
    for field in required_fields:
        if not data.get(field) or str(data[field]).strip() == "":
            response['success'] = False
            response['code'] = 400
            response['error'] = f"'{field}' is required and cannot be empty"
            return response

    file_url = None
    tkt_count = check_tkt_existed(data['author_id']) or 0

    ticket_code = f"{data['author_id']}_TKT{tkt_count+1:03d}"


    if file:
        print("INside the if file")
        # Clean file name
        name, ext = os.path.splitext(file.filename)
        name = re.sub(r'[^\w\-]', '_', name)
        clean_file_name = f"{name}{ext}"

        upload_dir = f"uploads/{data['author_id']}/{ticket_code}"
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, clean_file_name)

        file_url = f"uploads/{data['author_id']}/{ticket_code}/{clean_file_name}"

        with open(file_path, "wb") as f:
            f.write(file.file.read())

    res = entry_in_query_tkts(
        ticket_code,
        data['author_id'],
        data['book_id'],
        data['subject'],
        data['description'],
        data['category'],
        file_url
    )

    if res[0]:
        msg_id = save_converstion(res[0], data['author_id'], "author", data['description'])
    
    response['message'] = "Your ticket is generated with ticket code = " + res[0]
    return response


def tkts_listing(author_id, status_filter="", category_filter="", priority_filter="", start_date_tz="", end_date_tz=""):
    response = {
        "success": True,
        "code": 200,
        "message": "",
        "data": [],
        "error": None
    }

    if not author_id or author_id == "":
        response['success'] = False
        response['code'] = 400
        response['message'] = "Author id is missing"
        response['error'] = {
            "feild":"author_id"
        }
        return response

    if author_id.lower() != "all":
        is_author_exists = check_author(author_id)
        if not is_author_exists:
            response['message'] = "Target Author Not Found"
            response['code'] = 404
            response['success'] = False
            response['error'] = {"field": "author_id"}
            return response
    
    res = fetch_authors_tkt(author_id, status_filter, category_filter, priority_filter, start_date_tz, end_date_tz)

    if not res:
        response['success'] = False
        response['code'] = 200
        response['message'] = 'No tickets Found'
        return response
    
    response['message'] = "Successfully recived your tickets."
    response['data'] = res
    return response


# Get that chat history for author
def chat_history(tkt_code, access_by, author_id):
    response = {
        "success": True,
        "code": 200,
        "message": "",
        "data": {},
        "error": None
    }

    # if not author_id or author_id.strip() == "":
    #     response['success'] = False
    #     response['code'] = 400
    #     response['message'] = "Author id is missing"
    #     response['error'] = {
    #         "feild":"author_id"
    #     }
    #     return response

    if access_by == "author":
        is_author_exists = check_author(author_id)
        if not is_author_exists:
            response['message'] = "Unautherized Access"
            response['code'] = 401
            response['success'] = False
            return response
        
    if access_by == "admin":
        is_admin_exists = check_admin(author_id)
        if not is_admin_exists:
            response['message'] = "Unautherized Access"
            response['code'] = 401
            response['success'] = False
            return response
    
    if not tkt_code or tkt_code.strip() == "":
        response['success'] = False
        response['code'] = 400
        response['message'] = "Ticket Code is missing"
        response['error'] = {
            "feild":"tkt_code"
        }
        return response
    

    res = get_chat_history(tkt_code, access_by)

    if not res:
        response['code'] = 404
        response['message'] = "Unable to fetch chat data"
        response['error'] = {
            "field":"access_by"
        }
        return response
    
    response['data'] = res
    response['message'] = "Successfully fetched data."
    return response


# saving author chat history
def save_chat_history(data):
    response = {
        "success": True,
        "code": 200,
        "message": "",
        "data": {},
        "error": None
    }

    if data.sender_type.lower() == "author":
        is_author_exists = check_author(data.sender_id)
        if not is_author_exists:
            response['message'] = "Unautherized Access"
            response['code'] = 401
            response['success'] = False
            return response

    if not data.sender_id or data.sender_id == "":
        response['success'] = False
        response['code'] = 400
        response['message'] = "sender_id is missing. It can be author/admin"
        response['error'] = {
            "feild":"author_id"
        }
        return response
    
    if not data.ticket_code or data.ticket_code.strip() == "":
        response['success'] = False
        response['code'] = 400
        response['message'] = "Ticket Code is missing"
        response['error'] = {
            "feild":"tkt_code"
        }
        return response
    
    if not data.sender_type or data.sender_type.strip() == "":
        response['success'] = False
        response['code'] = 400
        response['message'] = "Sender type is missing. It can be author/admin"
        response['error'] = {
            "feild":"tkt_code"
        }
        return response

    res = save_chat(data.ticket_code, data.sender_id, data.sender_type, data.message)

    if not res:
        response['code'] = 422
        response['message'] = "Unbale to save chat"

    response['message'] = f"Message is saved with id {res[0]}"
    return response


def save_admin_actions(data):

    response = {
        "success": True,
        "code": 200,
        "message": "",
        "data": {},
        "error": None
    }

    if data.action not in ('status', 'priority', 'notes', 'assigned_by', 'assigned_to'):
        response['code'] = 401
        response['message'] = "Wrong action is send"
        response['error'] = {
            "field":"action"
        }
        return response

    res = save_action_for_tkt(data.ticket_code, data.action, data.action_val)

    if not res:
        response['code'] = 400
        response['message'] = "Unable to update"
        return response
    
    response["message"] = f"{data.ticket_code} successfully Updated."
    response["data"] = res[0]
    return response

def tktDetail_for_admin(admin_code, ticket_code):
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
    
    res = fetch_tkt_data_for_admin(ticket_code)

    if not res:
        response['code'] = 400
        response['message'] = "Unable to fetch the data"
        response['success'] = False
        return response
    
    response["message"] = f"{ticket_code} data successfully fetched."
    response["data"] = res
    return response
