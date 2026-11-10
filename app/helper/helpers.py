from app.db.db_connection import db_connection
from dotenv import load_dotenv
import os
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, Request, WebSocket

load_dotenv()

def check_author(author_id):
    con = db_connection()
    cur = con.cursor()

    cur.execute(
        """
            SELECT name FROM authors WHERE author_id = %s;
        """, (author_id,)
    )

    res = cur.fetchone()
    cur.close()
    con.close()
    return res[0]

def check_admin(admin_id):
    con = db_connection()
    cur = con.cursor()

    cur.execute(
        """
            SELECT name FROM admins WHERE admin_id = %s;
        """, (admin_id,)
    )

    res = cur.fetchone()
    cur.close()
    con.close()
    return res[0]


# generate jwt after successful login
def generate_token(user_id,role):

    expiry_date = datetime.now(timezone.utc) + timedelta(minutes=60)
    token = jwt.encode({"id":user_id, "role":role, "exp":expiry_date}, os.getenv('SECRET_KEY'), 'HS256')

    return token

def get_current_user(request: Request= None, websocket: WebSocket = None):
    token = None
    cookies = {}

    if request:
        cookies = request.cookies
    elif websocket:
        cookies = websocket.cookies

    if 'access_token_admin' in cookies:
        token = cookies['access_token_admin']
    elif 'access_token_author' in cookies:
        token = cookies['access_token_author']

    if not token:
        raise HTTPException(
            status_code=401,
            detail={
                "success": False,
                "code": 401,
                "data": {},
                "message": "Authentication failed",
                "error": "Not authenticated"
            }
        )
    try:
        payload = jwt.decode(
            token,
            os.getenv("SECRET_KEY"),
            algorithms=["HS256"]
        )
        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail={
                "success": False,
                "code": 401,
                "message": "Authentication failed",
                "data": {},
                "error": "Token expired"
            }
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail={
                "success": False,
                "code": 401,
                "message": "Authentication failed",
                "data": {},
                "error": "Invalid token"
            }
        )
    

def require_author(current_user = Depends(get_current_user)):
    
    if current_user['role'] != 'author':
        raise HTTPException(
            status_code=403,
            detail={
                "success": False,
                "code": 403,
                "message": "Autherization failed",
                "data": {},
                "error": "Unauthorized Access"
            }
        )
    
    if current_user['id'] != "" and current_user['id'] is not None:
        res = check_author(current_user['id'])
        if not res:
            raise HTTPException(
                status_code=401,
                detail={
                    "success": False,
                    "code": 401,
                    "message": "Authentication failed",
                    "data": {},
                    "error": f"This user_id {current_user['id']} is no longer exists"
                }
            )
        current_user['name'] = res
    
    return current_user

def require_admin(current_user = Depends(get_current_user)):
    
    if current_user['role'] != 'admin':
        raise HTTPException(
            status_code=403,
            detail={
                "success": False,
                "code": 403,
                "message": "Autherization failed",
                "data": {},
                "error": "Unauthorized Access"
            }
        )
    
    if current_user['id'] != "" and current_user['id'] is not None:
        res = check_admin(current_user['id'])
        if not res:
            raise HTTPException(
                status_code=401,
                detail={
                    "success": False,
                    "code": 401,
                    "message": "Authentication failed",
                    "data": {},
                    "error": f"This user_id {current_user['id']} is no longer exists"
                }
            )
        current_user['name'] = res
    
    return current_user