from fastapi import FastAPI
from app.modules.auth.auth_router import auth_router
from app.modules.tickets.tkt_router import tkt_router
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

app.include_router(auth_router,prefix='/auth', tags=['Auth'])

app.include_router(tkt_router, prefix="/ticket", tags=['Tickets'])

# connect upload with main app
os.makedirs("uploads", exist_ok=True) #when app run it will make upload folder
app.mount('/uploads', StaticFiles(directory="uploads"), name="uploads")