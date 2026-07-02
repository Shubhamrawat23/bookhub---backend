from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.modules.auth.auth_router import auth_router
from app.modules.tickets.tkt_router import tkt_router
from app.modules.books.book_router import book_router
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://bookhub-front-end.vercel.app"
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

app.include_router(book_router, prefix="/author", tags=['Books'])

# connect upload with main app
os.makedirs("uploads", exist_ok=True) #when app run it will make upload folder
app.mount('/uploads', StaticFiles(directory="uploads"), name="uploads") #define url path to folder where '1 param' is the URL prefix means after domain it will start from there, '2 param' is for fastapi to fetch data from this local dirs as acc. to url and '3 param' is for fetch directly from name (as shortcut)