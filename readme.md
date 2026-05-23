# BookLeaf Assignment Backend

Backend service for the BookLeaf Author & Admin Support System built using FastAPI and PostgreSQL.

---

# Live Demo Links

## Frontend Application

#### Author Login
https://bookleafpub-frontend.vercel.app or https://bookleafpub-frontend.vercel.app/author/login

#### Admin Login
https://bookleafpub-frontend.vercel.app/admin/login

## Backend API Domian

https://bookleafpub-backend-production.up.railway.app

## Swagger API Documentation

https://bookleafpub-backend-production.up.railway.app/docs

---

# Test Credentials

## Author Portal

Email: priya.sharma@email.com  
Password: 123456

#### Note: You can create/update new password for other authors also through forgot password (https://bookleafpub-frontend.vercel.app/author/forgot-password)
---

## Admin Portal

#### ADMIN 1
Email: admin_00001@bookleafpub.com  
Password: admin@123

#### ADMIN 2
Email: admin_00002@bookleafpub.com  
Password: admin002@123

---

# Project Overview

This project is a support and management system for BookLeaf publishers.

The platform includes:

- Author Portal
- Admin Portal
- Book Management
- Support Ticket System
- Ticket Chat System

The backend exposes REST APIs using FastAPI and stores data using PostgreSQL.

---

# Tech Stack

## Backend

- Python
- FastAPI
- PostgreSQL
- Pydantic
- Uvicorn
- psycopg2
- python-dotenv
- python-multipart

---

# Deployment Notes

- Backend deployed on Railway
- PostgreSQL hosted on Railway PostgreSQL
- Frontend deployed on Vercel
- Environment variables configured securely through Railway/Vercel dashboards
- Configured CORS handling between Railway backend and Vercel frontend

---

# Project Structure

```text
backend/
│
├── app/
│   ├── main.py
│   │
│   ├── db/
│   │   ├── db_connection.py
│   │   ├── init_db.py
│   │   └── seed_db.py
│   │
│   ├── helpers/
│   │
│   ├── modules/
│   │   ├── auth/
│   │   │   ├── auth_routes.py
│   │   │   ├── auth_service.py
│   │   │   ├── auth_repository.py
│   │   │   └── auth_schemas.py
│   │   │
│   │   ├── books/
│   │   │
│   │   ├── tickets/
│   │   │
│   │   └── admin/
│   │
│   └── config/
│
├── requirements.txt
└── README.md
```


![alt text](<shape_a4eYW-9ecbZbpZHYsxNv5 at 26-05-23 18.58.24.png>)

---

# Architecture Decisions

The backend follows a feature-based modular architecture for scalability and maintainability.

---

# Architecture Layers

## Routes Layer

Handles API endpoints and request routing.

## Schemas Layer

Handles request/response validation and data typing using Pydantic BaseModel schemas.

## Service Layer

Contains business logic and validations.

## Repository Layer

Handles direct PostgreSQL database operations.

---

# Request Flow

```text
Frontend
   ↓
FastAPI Routes
   ↓
Schemas Layer
   ↓
Service Layer
   ↓
Repository Layer
   ↓
PostgreSQL Database
```

---

# Features Implemented

## Authentication

## Author Side

- Author login
- Forgot password
- Password reset
- Password hashing using SHA256 (implemented for assignment MVP scope)

## Admin Side

- Admin login
- Password hashing using SHA256 (implemented for assignment MVP scope)
- Admin ticket management

---

# Book Management

- Fetch author books
- Book metadata handling
- Royalty information handling

---

# Ticket Management

- Create support tickets
- Fetch author tickets
- Ticket status updates
- Ticket message/chat system
- Admin ticket management
- Ticket priority handling

---

# Database Structure

# Main Tables

## authors

Stores author information.

## books

Stores author books and royalty-related information.

## query_tickets

Stores support tickets raised by authors.

## ticket_messages

Stores ticket message/chat history.

## admins

Stores admin credentials and management information.

---

# Environment Variables

Create a `.env` file inside backend root.

Example:

```env
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

---

# Install Dependencies

Create virtual environment:

```bash
python -m venv venv
```

---

# Activate Virtual Environment

## Windows

```bash
venv\Scripts\activate
```

---

# Install Requirements

```bash
pip install -r requirements.txt
```

---

# Python Requirements

```txt
annotated-doc==0.0.4
annotated-types==0.7.0
anyio==4.13.0
click==8.4.0
colorama==0.4.6
fastapi==0.136.1
h11==0.16.0
idna==3.15
psycopg2-binary==2.9.12
pydantic==2.13.4
pydantic_core==2.46.4
python-dotenv==1.2.2
python-multipart==0.0.29
starlette==1.0.0
typing-inspection==0.4.2
typing_extensions==4.15.0
uvicorn==0.47.0
```

---

# Database Setup

## Create Database

```sql
CREATE DATABASE bookleaf_db;
```

---

# Initialize Database Tables

Run from backend root:

```bash
python -m app.db.init_db
```

---

# Seed Database

Run from backend root:

```bash
python -m app.db.seed_db
```

This seeds:

- Authors
- Books
- Admins
- Sample ticket data

---

# Run Backend Server

From backend root:

```bash
uvicorn app.main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

---

# API Documentation

FastAPI automatically generates Swagger/OpenAPI documentation.

## Local Swagger Docs

```text
http://127.0.0.1:8000/docs
```

---

## Live Swagger Docs

```text
https://your-backend.up.railway.app/docs
```

---

# API Endpoints

# Authentication APIs

## Author Login

### POST

```text
/auth/author/login
```

Body:

```json
{
  "email": "priya.sharma@email.com",
  "password": "123456"
}
```

---

## Forgot Password

### POST

```text
/auth/author/forgot-password
```

Body:

```json
{
  "email": "author@test.com",
  "new_password": "123456",
  "confirm_password": "123456"
}
```

---

## Admin Login

### POST

```text
/auth/admin/login
```

Body:

```json
{
  "email": "admin@test.com",
  "password": "admin123"
}
```

---

# Books APIs

## Fetch Author Books

### GET

```text
/author/book/list?author_id=
```

---

# Ticket APIs

## Create Ticket

### POST

```text
/ticket/create
```

---

## Fetch Author Tickets

### GET

```text
/ticket/author/list?author_id=
```

---

## Fetch Ticket Messages

### GET

```text
/ticket/messages?ticket_code=
```

---

## Send Ticket Message

### POST

```text
/ticket/message/send
```

---

# Admin APIs

## Fetch All Tickets

### GET

```text
/admin/tickets
```

---

## Update Ticket Status

### PUT

```text
/admin/ticket/status
```

---

# Standard API Response Format

All APIs return standardized JSON responses.

Example:

```json
{
  "success": true,
  "code": 200,
  "message": "Success",
  "data": {},
  "error": null
}
```


# Known Limitations

- JWT/session token authentication not implemented yet
- Polling used instead of WebSockets
- Basic session handling
- No notification system yet

---

# Future Improvements

- JWT/session token Authentication
- Role-based authorization
- WebSocket real-time updates
- Redis caching
- Notification system
- File upload optimization
- Docker support
- CI/CD pipeline
- Advanced filtering/search
- Analytics dashboard
- AI-powered ticket categorization
- AI-generated admin reply suggestions

---

# Development Notes

## Design Decisions

- FastAPI chosen for speed and automatic OpenAPI documentation
- PostgreSQL chosen for relational consistency
- Railway used for backend/database deployment
- Feature-based architecture improves scalability
- Zustand used on frontend for lightweight session management

---

# Tradeoffs

- Polling used instead of WebSockets for simplicity
- Focused on core functionality over advanced animations
- Lightweight authentication used for MVP assignment scope

---

# Production Improvements

If evolving this project further into production:

- Implement JWT refresh token flow
- Add RBAC authorization
- Introduce Docker containers
- Add Redis queues/caching
- Move to WebSocket-based live messaging
- Add centralized logging and monitoring
- Add automated testing and CI/CD



---

Built as part of the BookLeafPub Full Stack Assignment.