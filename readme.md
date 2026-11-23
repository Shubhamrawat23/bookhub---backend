# Bookhub Assignment Backend

Backend service for the Bookhub Author & Admin Support System built using FastAPI, PostgreSQL, and Docker. Features secure HttpOnly cookie authentication, real-time WebSocket chat, and a fully automated CI/CD deployment pipeline to an Azure Virtual Machine.

---

# Live Demo Links

## Frontend Application

#### Author Login
https://bookhubdev.site/ or https://bookhubdev.site/author/login

#### Admin Login
https://bookhubdev.site/admin/login

## Swagger API Documentation

<!-- https://bookhub-back-end-production.up.railway.app/docs -->
https://bookhubdev.site/api

---

# Test Credentials

## Author Portal

Email: sa@email.com  
Password: 123456

---

## Admin Portal

#### ADMIN 1
Email: admin_00001@bookhub.com  
Password: admin@123

#### ADMIN 2
Email: admin_00002@bookhub.com  
Password: admin002@123

---

# Project Overview

This project is a support and management system for Bookhub publishers.

The platform includes:

- Author Portal
- Admin Portal
- Book Management
- Support Ticket System
- Real-time Ticket Chat System (WebSockets)

The backend exposes REST APIs using FastAPI and stores data using PostgreSQL. It is fully containerized using Docker and deployed via an automated CI/CD pipeline.

---

# Tech Stack

## Backend

- Python
- FastAPI
- PostgreSQL
- Pydantic
- Uvicorn
- psycopg2
- PyJWT (JWT Authentication)
- python-dotenv
- python-multipart
- WebSockets

---

## DevOps & Infrastructure
- **Containerization:** Docker & Docker Compose
- **CI/CD:** GitHub Actions
- **Hosting:** Azure Virtual Machine (Ubuntu 24.04)
- **Web Server / Proxy:** Nginx (SSL Termination, WebSocket Upgrade)
- **Database Persistence:** Docker Named Volumes (`bookhub_vol`)
- **Security:** GitHub Secrets (Runtime injection), Azure NSG, UFW, Let's Encrypt

---

# DevOps & Architecture Highlights

1. **Multi-Container Architecture:** The backend runs alongside a PostgreSQL container. The database is hidden from the public internet and only accessible on an internal Docker network (`bookhub_net`).
2. **Zero-Downtime Migrations:** The CI/CD pipeline deploys a dedicated `init_db_seed_db` container on every push. The scripts (`init_db.py` and `seed_db.py`) are designed to be **idempotent** (using `IF NOT EXISTS` and `ON CONFLICT DO NOTHING`), ensuring deployments never crash due to existing data.
3. **WebSocket & Nginx Integration:** The backend exposes WebSocket endpoints. The frontend Nginx container is configured with `proxy_http_version 1.1`, `Upgrade`, and `Connection "upgrade"` headers to seamlessly proxy WebSocket traffic to FastAPI.
4. **Secure Secret Management:** Database passwords and the JWT `SECRET_KEY` are never stored in the repository. They are injected into the Azure VM at runtime via GitHub Secrets using `export` variables during the SSH deployment step.
5. **Persistent File Storage:** Uploaded ticket attachments are stored in a Docker named volume (`tkt_uploads_vol`), decoupling data persistence from the container lifecycle.

---

# CI/CD Pipeline (`.github/workflows/back_deploy.yml`)

The GitHub Actions pipeline performs the following:
1. **Testing:** Spins up a PostgreSQL service container, runs `flake8` for syntax checks, and executes `pytest` for unit and integration testing.
2. **Deployment:** 
   - Uses `appleboy/scp-action` to securely copy the latest code to the Azure VM.
   - SSHes into the VM, exports the environment variables from GitHub Secrets, and runs `docker compose up -d --build`.

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


![alt text](architectureflow.png)

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
FastAPI Routes (REST / WebSocket)
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

## Authentication & Security

- HttpOnly Cookie Auth: JWT tokens are securely stored in HttpOnly, Secure, SameSite=None cookies (eliminates XSS token theft).

- Role-Based Access Control (RBAC): Distinct require_admin and require_author dependencies.

- WebSocket Auth: WebSocket connections are authenticated by reading the HttpOnly cookie during the handshake.

- Global Exception Handling: All errors (Pydantic 422, HTTPExceptions, Internal 500s) return a unified, predictable JSON format for the frontend.



## Author Side

- Author login, forgot password, and password reset
- Fetch author books and metadata
- Create support tickets
- Fetch author tickets

## Admin Side

- Admin login
- Admin ticket management


## Book Management

- Fetch author books
- Book metadata handling
- Royalty information handling


## Ticket Management & Real-Time Chat

- Create support tickets
- Fetch author tickets
- Ticket status updates
- Ticket message/chat system
- Admin ticket management
- Ticket priority handling
- Real-time WebSocket Chat: Live bi-directional messaging between Authors and Admins using a Room-based Connection Manager (ws_manager).

## WebSocket Endpoints
The chat system bypasses HTTP polling and uses persistent WebSocket connections.

 - Author Chat: ws://domain/api/ticket/ws/author/chat/{ticket_code}

 - Admin Chat: ws://domain/api/ticket/ws/admin/chat/{ticket_code}

Note: Authentication is handled automatically by the browser via the HttpOnly cookie during the WebSocket handshake.



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
PyJWT==2.13.0
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
CREATE DATABASE bookhub_db;
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
  "email": "sa001@email.com",
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
  "email": "admin_00001@bookhub.com",
  "password": "admin@123"
}
```

---

## Get Current User

### GET

```text
/auth/me
```

Reads HttpOnly cookie to return current logged-in user details (id, role, name).

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
/ticket/author/list
```

---

## Fetch Ticket Messages

### GET

```text
/ticket/messages?ticket_code={code}
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

- WebSocket Connection Manager is stored in-memory (requires Redis Pub/Sub for multi-server scaling).
- No notification system yet

---

# Future Improvements

- Refresh Token rotation for extended sessions.
- Redis Pub/Sub for horizontally scaling WebSockets.
- AI-powered ticket categorization
- AI-generated admin reply suggestions
- Image Storage: Migrate from local Docker volumes to Cloud Storage to decouple user uploads from the VM disk.



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

- WebSockets chosen over polling for real-time chat to improve UX and reduce server load, at the cost of needing to manage persistent connections.

- Focused on core functionality over advanced animations.



---

# Production Improvements

If evolving this project further into production:

- Implement Database Migrations (Alembic) instead of raw init scripts.
- Add Redis for WebSocket message brokering.



---