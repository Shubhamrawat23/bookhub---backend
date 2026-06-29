from app.db.db_connection import db_connection
from dotenv import load_dotenv
import os
import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from fastapi import HTTPException

load_dotenv()

def check_author(author_id):
    con = db_connection()
    cur = con.cursor()

    cur.execute(
        """
            SELECT EXISTS(SELECT 1 FROM authors WHERE author_id = %s);
        """, (author_id,)
    )

    res = cur.fetchone()
    cur.close()
    con.close()
    return bool(res[0])

def check_admin(admin_code):
    con = db_connection()
    cur = con.cursor()

    cur.execute(
        """
            SELECT EXISTS(SELECT 1 FROM admins WHERE admin_code = %s);
        """, (admin_code,)
    )

    res = cur.fetchone()
    cur.close()
    con.close()
    return bool(res[0])


# generate jwt after successful login
def generate_token(user_id,role):

    expiry_date = datetime.now() + timedelta(minutes=60)
    token = jwt.encode({"id":user_id, "role":role, "exp":expiry_date}, os.getenv('SECRET_KEY'), 'HS256')

    return token


OAuth_Schema = OAuth2PasswordBearer(tokenUrl='/login')

def get_current_user(token: str = Depends(OAuth_Schema)):
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
            detail="Token expired"
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    

def require_author(current_user = Depends(get_current_user)):
    
    if current_user['roles'] != 'author':
        raise HTTPException(
            status_code=403,
            detail="Unauthorized Access"
        )
    
    return current_user

def require_admin(current_user = Depends(get_current_user)):
    
    if current_user['roles'] != 'admin':
        raise HTTPException(
            status_code=403,
            detail="Unauthorized Access"
        )
    
    return current_user