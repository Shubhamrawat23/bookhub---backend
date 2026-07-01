from pydantic import BaseModel

class SaveMessage(BaseModel):
    ticket_code: str
    message: str

class TktActions(BaseModel):
    ticket_code: str 
    action: str 
    action_val: str | int