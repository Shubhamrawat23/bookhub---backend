from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from app.modules.auth.auth_router import auth_router
from app.modules.tickets.tkt_router import tkt_router
from app.modules.books.book_router import book_router
from fastapi.staticfiles import StaticFiles
import os
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://bookhub-front-end.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router,prefix='/auth', tags=['Auth'])

app.include_router(tkt_router, prefix="/ticket", tags=['Tickets'])

app.include_router(book_router, prefix="/author", tags=['Books'])



# Handle HTTPExceptions (401, 403, 404, etc.)
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    # If you passed a dictionary as detail (like in your helpers.py), use it.
    # Otherwise, wrap the string detail in your standard format.
    if isinstance(exc.detail, dict):
        error_data = exc.detail
    else:
        error_data = {
            "success": False,
            "code": exc.status_code,
            "message": "Authentication Error" if exc.status_code == 401 else "Error",
            "data": {},
            "error": exc.detail
        }
        
    return JSONResponse(
        status_code=exc.status_code,
        content=error_data
    )

# Handle Pydantic Errors (422)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Extract the first error message to make it readable for the frontend
    error_msg = exc.errors()[0].get("msg", "Invalid input data")
    field = exc.errors()[0].get("loc", ["unknown"])[-1] # Gets the field name
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "code": 422,
            "message": "Validation failed",
            "data": {},
            "error": {
                "field": field,
                "detail": error_msg
            }
        }
    )

# Handle 500 Internal Server Errors (Bugs)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # In production, you would log `exc` to Sentry or Datadog here!
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "code": 500,
            "message": "Internal Server Error",
            "data": {},
            "error": "Something went wrong on our end. Please try again later."
        }
    )


# connect upload with main app
os.makedirs("uploads", exist_ok=True) #when app run it will make upload folder
app.mount('/uploads', StaticFiles(directory="uploads"), name="uploads") #define url path to folder where '1 param' is the URL prefix means after domain it will start from there, '2 param' is for fastapi to fetch data from this local dirs as acc. to url and '3 param' is for fetch directly from name (as shortcut)