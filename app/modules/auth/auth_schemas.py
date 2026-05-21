from pydantic import BaseModel

class UserLogin(BaseModel):
    email: str
    password: str

class ForgetPassword(BaseModel):
    email: str
    new_password: str
    confirm_password: str