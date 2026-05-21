from fastapi import APIRouter
from app.modules.auth.auth_schemas import ForgetPassword
from app.modules.auth.auth_schemas import UserLogin
from app.modules.auth.auth_service import forgot_Password
from app.modules.auth.auth_service import author_login
from app.modules.auth.auth_service import admin_login

auth_router = APIRouter()


@auth_router.post("/author/login")
def author_login_route(data: UserLogin):
    response = author_login(data)
    return response

@auth_router.post("/author/forgot-password")
def author_forgot_password_route(data: ForgetPassword):
    response = forgot_Password(data)

    return response

@auth_router.post("/admin/login")
def admin_login_route(data: UserLogin):
    response = admin_login(data)
    return response