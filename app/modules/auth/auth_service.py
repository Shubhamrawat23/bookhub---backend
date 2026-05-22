from app.modules.auth.auth_repository import author_forgot_password
from app.modules.auth.auth_repository import authorLogin
from app.modules.auth.auth_repository import adminLogin
import hashlib

# author login
def author_login(data):
    response = {
        "success": True,
        "code": 200,
        "message": "",
        "data": {},
        "error": None
    }

    author_hash_password = hashlib.sha256(data.password.encode()).hexdigest()

    resp = authorLogin(data.email)
    if not resp:
        response['success'] = False
        response['code'] = 404
        response['message'] = "Email not found"
        response['error'] = {
            "field": "email"
        }
        return response
    
    if (resp[4] != author_hash_password):
        response['success'] = False
        response['code'] = 422
        response['message'] = "Wrong Password"
        response['error'] = {
            "field": "password"
        }
        return response
    
    response['message'] = "Successfully Login"
    return response

# author forgot password
def forgot_Password(data):
    response = {
        "success": True,
        "code": 200,
        "message": "",
        "data": {},
        "error": None
    }

    print(data)
    
    if (data.confirm_password != data.new_password):
        response['success'] = False
        response['message'] = "New and Confirm Passwords are not same."
        response['code'] = 422
        return response
    
    hash_pswrd = hashlib.sha256(data.new_password.encode()).hexdigest()
    resp = author_forgot_password(data.email, hash_pswrd)
    print(resp)

    if not resp:
        response['success'] = False
        response['code'] = 404
        response['message'] = "Email not found"
        response['error'] = {
            "field": "email"
        }
        return response
    
    response['message'] = "Password updated successfully"
    response['data'] = {
        "email": data.email
    }
    return response


# Admin login
def admin_login(data):
    response = {
        "success": True,
        "code": 200,
        "message": "",
        "data": {},
        "error": None
    }

    admin_hash_password = hashlib.sha256(data.password.encode()).hexdigest()

    resp = adminLogin(data.email)
    if not resp:
        response['success'] = False
        response['code'] = 404
        response['message'] = "Email not found"
        response['error'] = {
            "field": "email"
        }
        return response
    
    if (resp[3] != admin_hash_password):
        response['success'] = False
        response['code'] = 401
        response['message'] = "Wrong Password"
        response['error'] = {
            "field": "password"
        }
        return response
    
    response['message'] = "Successfully Login"
    return response