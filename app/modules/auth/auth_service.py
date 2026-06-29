from app.modules.auth.auth_repository import author_forgot_password
from app.modules.auth.auth_repository import authorLogin
from app.modules.auth.auth_repository import adminLogin
import hashlib
from app.helper.helpers import generate_token

# author login
def author_login(data):
    response = {
        "success": True,
        "code": 200,
        "message": "",
        "data": {},
        "error": None
    }

    if(len(data.password)<6):
        response['success'] = False
        response['code'] = 422
        response['message'] = "Password lenght should be more than 6."
        response['error'] = {
            "field": "password"
        }
        return response


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
        response['code'] = 401
        response['message'] = "Wrong Password"
        response['error'] = {
            "field": "password"
        }
        return response
    
    if resp[0]:
        token = generate_token(resp[0],'author')

    response['message'] = "Successfully Login"
    response['data'] = {
        "author_id": resp[0],
        "name": resp[1],
        "email": resp[2],
        "phone": resp[3],
        "access_token":token,
        "token_type":'bearer'
    }
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
    
    if(len(data.confirm_password)<6 and len(data.new_password)<6):
        response['success'] = False
        response['code'] = 422
        response['message'] = "Password lenght should be more than 6."
        response['error'] = {
            "field": "new_password and confirm_password"
        }
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
    
    if (resp[4] != admin_hash_password):
        response['success'] = False
        response['code'] = 422
        response['message'] = "Wrong Password"
        response['error'] = {
            "field": "password"
        }
        return response
    
    if resp[0]:
        token = generate_token(resp[0],'admin')
    
    response['message'] = "Successfully Login"
    response['data'] = {
        "admin_id":resp[0],
        "admin_code": resp[1],
        "name": resp[2],
        "email": resp[3],
        "access_token":token,
        "token_type":'bearer'
    }
    return response