# BookLeaf Assignment Backend

Backend service for BookLeaf author support system built using FastAPI and PostgreSQL.

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- Pydantic
- Uvicorn
- hashlib (password hashing for assignment MVP)

---

## Project Structure

backend/<br>
├── app/<br>
│   ├── main.py <br>
│   ├── db/ <br>
│   │   ├── init_db.py <br>
│   │   ├── db_connection.py <br> 
│   │   └── seed_db.py <br>
│   ├── modules/ <br>
│   │   └── auth/ <br>
│   │       ├── auth_routes.py <br>
│   │       ├── auth_service.py <br>
│   │       ├── auth_repository.py <br>
│   │       └── auth_schemas.py <br>
└── requirements.txt <br>

---

## Features Implemented

### Authentication

Author side:

- Author login
- Forgot password
- Password hashing using SHA256

Admin side:

- Admin login

---

## Database Setup

Create PostgreSQL database:

```sql
CREATE DATABASE bookleaf_db;
```

Update database credentials in:

`app/db/db_connection.py`

Example:

```python
host=""
database=""
user=""
password=""
port=""
```

---

## Seed Database

Seed authors/books/admins into database.

Run from backend root:

```bash
python -m app.db.seed_db
```

---

## Install Dependencies

Create virtual environment:

```bash
python -m venv venv
```

Activate:

### Windows

```bash
venv\Scripts\activate
```

Install packages:

```bash
pip install fastapi uvicorn psycopg2 pydantic
```

---

## Run Backend

From backend root:

```bash
uvicorn app.main:app --reload
```

---

## API Docs

Swagger docs:

```text
http://127.0.0.1:8000/docs
```

---

## Current API Endpoints

### Auth

### Author login

POST

```text
/auth/login
```

Body:

```json
{
  "email": "priya.sharma@email.com",
  "password": "123456"
}
```

---

### Forgot password

POST

```text
/auth/forgot-password
```

Body:

```json
{
  "email": "priya.sharma@email.com",
  "new_password": "123456",
  "confirm_password": "123456"
}
```

---

## Response Format

All APIs return standardized JSON response:

```json
{
  "success": true,
  "code": 200,
  "message": "",
  "data": {},
  "error": null
}
```

---

## Planned Modules

- Author books dashboard
- Support ticket creation
- Ticket messages
- Admin ticket management
- AI categorization
- Internal notes
- Reopen ticket support

---

## Development Notes

Architecture used:

Feature-based modular backend.

Layers:

- Routes → API endpoints
- Service → business logic
- Repository → database queries

Flow:

Frontend → Route → Service → Repository → PostgreSQL

---