from fastapi import APIRouter, Form, File, UploadFile, Query, Depends, WebSocket, WebSocketDisconnect
from app.modules.tickets.tkt_service import create_tkt, tkts_listing, chat_history, save_chat_history, save_admin_actions, tktDetail_for_admin
from app.modules.tickets.tkt_schemas import SaveMessage, TktActions
from app.helper.helpers import check_admin, require_author, require_admin
import json
from fastapi.encoders import jsonable_encoder
from starlette.concurrency import run_in_threadpool

tkt_router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, tkt_code: str, websocket: WebSocket):
        await websocket.accept()
        if tkt_code not in self.active_connections:
              self.active_connections[tkt_code] = []
        self.active_connections[tkt_code].append(websocket)

    def disconnect(self,tkt_code: str, websocket: WebSocket):
        if tkt_code in self.active_connections:
                if websocket in self.active_connections[tkt_code]:
                    self.active_connections[tkt_code].remove(websocket)
        if not self.active_connections[tkt_code]:
            del self.active_connections[tkt_code]

    async def broadcast(self, tkt_code: str, message: str):
        if tkt_code in self.active_connections:
            for connection in self.active_connections[tkt_code]:
                await connection.send_text(message)

ws_manager = ConnectionManager()

async def handle_chat_session(websocket: WebSocket, ticket_code: str, current_user: dict):
    await ws_manager.connect(ticket_code, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            msg = data.get("message")
            
            if not msg:
                continue

            db_data = {
                "ticket_code": ticket_code,
                "message": msg,
                "sender_id": current_user['id'],
                "sender_type": current_user['role']
            }
            response = save_chat_history(db_data)
            # response = await run_in_threadpool(save_chat_history, db_data)

            if response['success']:
                payload = {
                    "id": response['data']['id'],
                    "sender_type": current_user['role'],
                    "sender": current_user['name'],
                    "message": msg,
                    "created_at": response['data']['created_at']
                }
                await ws_manager.broadcast(ticket_code, json.dumps(jsonable_encoder(payload)))
                
    except WebSocketDisconnect:
        ws_manager.disconnect(ticket_code, websocket)

@tkt_router.post("/author/create")
def author_create_tkt_route(
    author_id: str = Form(None),
    book_id: str = Form(...),
    subject: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    file: UploadFile = File(None),
    current_user = Depends(require_author)
    ):
    
        data = {
            "author_id": current_user['id'],
            "book_id": book_id,
            "subject": subject,
            "description": description,
            "category": category,
        }
        response = create_tkt(data, file)
        return response

@tkt_router.get("/author/list")
def tkts_author_route(current_user: str=Depends(require_author)):
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
        
        response = tkts_listing(current_user['id'], current_user['role'])
        return response

@tkt_router.get("/author/tkt_chat")
def tkt_chat_history_author_route(tkt_code: str = Query(...), access_by: str = Query(None), author_id: str = Query(None), current_user = Depends(require_author)):
        response = chat_history(tkt_code, current_user['role'], current_user['id'])

        return response


# add websocket for author chat 
@tkt_router.websocket("/ws/author/chat")
async def save_author_chat_history_route(websocket: WebSocket, ticket_code: str, current_user: str= Depends(require_author)):
        await handle_chat_session(websocket, ticket_code, current_user)



# get tkts list for admins

@tkt_router.get("/admin/list")
def tkts_admin_route(
        author_id: str = Query(None), # send 'all'
        admin_code: str = Query(None),
        status_filter: str = Query(""), 
        category_filter: str = Query(""), 
        priority_filter: str = Query(""), 
        start_date_tz: str = Query(""), 
        end_date_tz: str = Query(""),
        current_user = Depends(require_admin)
    ):


        # is_admin_exists = check_admin(admin_code)
        # if not is_admin_exists:
        #         response['message'] = "Unautherized Access"
        #         response['code'] = 401
        #         response['success'] = False
        #         return response

        # if (author_id.lower()) != "all":
        #     response['success'] = False
        #     response['code'] = 401
        #     response['message'] = "Unautherized Access"
        #     response['error'] = {
        #             "field":"author_id"
        #     }
        #     return response
        
        response = tkts_listing(current_user['id'], current_user['role'], status_filter, category_filter, priority_filter, start_date_tz, end_date_tz)
        return response


# get chat history for admin
@tkt_router.get("/admin/tkt_chat")
def tkt_chat_history_admin_route(tkt_code: str = Query(...), access_by: str = Query(None),author_id: str = Query(None), current_user = Depends(require_admin)):
        
        # response = {
        #     "success": True,
        #     "code": 200,
        #     "message": "",
        #     "data": {},
        #     "error": None
        # }

        # if (access_by.lower()) != "admin":
        #     response['success'] = False
        #     response['code'] = 401
        #     response['message'] = "Unautherized Access"
        #     response['error'] = {
        #             "field":"access_by"
        #     }
        #     return response
        
        response = chat_history(tkt_code, current_user['role'], current_user['id'])
        return response


# add websocket admin chat
@tkt_router.websocket("/ws/admin/chat")
async def save_admin_chat_history_route(websocket: WebSocket, ticket_code: str, current_user = Depends(require_admin)):
    await handle_chat_session(websocket, ticket_code, current_user)

# save admin actions

@tkt_router.put("/admin/tkt_action")
def admin_actions_route(data: TktActions, current_user = Depends(require_admin)):
       resposne = save_admin_actions(data)
       return resposne

# get tkt data for admin
@tkt_router.get('/admin/tkt_detail')
def tktDetail_for_admin_route(ticket_code:str, current_user: str = Depends(require_admin)):
       response = tktDetail_for_admin(ticket_code)
       return response