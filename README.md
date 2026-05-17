# Nimap FastAPI Machine Test

REST API for managing Users, Clients, and Projects with JWT authentication.

## Tech Stack
- **FastAPI** — web framework
- **SQLAlchemy 2.x** — ORM
- **MySQL** — database (PostgreSQL also supported)
- **JWT (python-jose)** — authentication
- **Passlib + bcrypt** — password hashing

## Project Structure

```
nimap/
├── app/
│   ├── core/
│   │   ├── config.py        # pydantic-settings (.env loader)
│   │   └── security.py      # JWT encode/decode, password hashing
│   ├── models/
│   │   ├── associations.py  # project_users many-to-many table
│   │   ├── user.py
│   │   ├── client.py
│   │   └── project.py
│   ├── schemas/
│   │   ├── user.py          # UserCreate, UserResponse, Token
│   │   ├── client.py        # ClientCreate, ClientUpdate, ClientResponse
│   │   └── project.py       # ProjectCreate, ProjectResponse
│   ├── routers/
│   │   ├── auth.py          # POST /auth/login
│   │   ├── users.py         # POST /users/  GET /users/
│   │   ├── clients.py       # CRUD /clients/
│   │   └── projects.py      # POST/GET/DELETE /projects/
│   ├── database.py          # SQLAlchemy engine + Base
│   ├── dependencies.py      # get_db, get_current_user
│   └── main.py              # FastAPI app, router registration
├── .env                     # environment variables
├── requirements.txt
└── README.md
```

## Setup & Run

### 1. Create the database

```sql
CREATE DATABASE nimap;
```

### 2. Configure `.env`

Edit `.env` with your database credentials:

```
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/nimap
SECRET_KEY=change-this-to-a-long-random-secret-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start server

```bash
uvicorn app.main:app --reload
```

Server runs at: `http://127.0.0.1:8000`

Tables are auto-created on startup via `Base.metadata.create_all()`.

## API Testing

Open Swagger UI: `http://127.0.0.1:8000/docs`

### Quick flow

1. **Register a user** — `POST /users/`
2. **Login** — `POST /auth/login` → copy the `access_token`
3. **Authorize in Swagger** — click **Authorize**, paste `Bearer <token>`
4. **Create a client** — `POST /clients/`
5. **Create a project** — `POST /projects/` with `client_id` and `users` list
6. **List your projects** — `GET /projects/` (returns only projects you're assigned to)

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/users/` | No | Register user |
| GET | `/users/` | No | List all users |
| POST | `/auth/login` | No | Login, get JWT |
| POST | `/clients/` | Yes | Create client |
| GET | `/clients/` | No | List all clients |
| GET | `/clients/{id}` | No | Client detail with projects |
| PUT/PATCH | `/clients/{id}` | Yes | Update client |
| DELETE | `/clients/{id}` | Yes | Delete client (204) |
| POST | `/projects/` | Yes | Create project |
| GET | `/projects/` | Yes | List my assigned projects |
| DELETE | `/projects/{id}` | Yes | Delete project (204) |
