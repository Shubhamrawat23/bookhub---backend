from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.modules.auth.auth_router import auth_router
from app.modules.tickets.tkt_router import tkt_router
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['POST', 'GET', 'PUT'],
    allow_headers=["*"],
)

app.include_router(auth_router,prefix='/auth', tags=['Auth'])

app.include_router(tkt_router, prefix="/ticket", tags=['Tickets'])

# connect upload with main app
os.makedirs("uploads", exist_ok=True) #when app run it will make upload folder
app.mount('/uploads', StaticFiles(directory="uploads"), name="uploads")