from fastapi import APIRouter, Response, Depends
from app.modules.auth.auth_schemas import ForgetPassword
from app.modules.auth.auth_schemas import UserLogin
from app.modules.auth.auth_service import forgot_Password
from app.modules.auth.auth_service import author_login
from app.modules.auth.auth_service import admin_login
import app.helper.helpers as helper

auth_router = APIRouter()


@auth_router.post("/author/login")
def author_login_route(data: UserLogin, response: Response):
    res = author_login(data)

    if res.get('success') and res.get('data', {}).get('access_token'):
        token = res['data']['access_token']
        response.set_cookie(
            key="access_token_author",
            value=token,
            httponly=True,
            secure=True,
            max_age=3600
        )

        del res['data']['access_token']

    return res

@auth_router.post("/author/forgot-password")
def author_forgot_password_route(data: ForgetPassword):
    response = forgot_Password(data)

    return response

@auth_router.post("/admin/login")
def admin_login_route(data: UserLogin, response: Response):
    result = admin_login(data)

    if result.get("success") and result.get('data',{}).get('access_token'):
        token = result['data']['access_token']

        response.set_cookie(
            key="access_token_admin",
            value=token,
            httponly=True,
            secure=True,
            max_age=3600
        )

        del result['data']['access_token']

    return result

@auth_router.post("/author/logout")
def user_logout(response: Response, current_user = Depends(helper.get_current_user)):
    response.delete_cookie(
        key="access_token_author",
        path="/",
        secure=True,
        httponly=True,
    )
    return {"success": True, "message": "Logged out successfully"}

@auth_router.post("/admin/logout")
def user_logout(response: Response, current_user = Depends(helper.get_current_user)):
    response.delete_cookie(
        key="access_token_admin",
        path="/",
        secure=True,
        httponly=True,
    )
    return {"success": True, "message": "Logged out successfully"}

@auth_router.get("/me")
def get_me(current_user = Depends(helper.get_current_user)):
    return {
        "code":200,
        "success": True,
        "data": current_user,
        "error": None
    }