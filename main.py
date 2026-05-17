from fastapi import FastAPI

from app.database import Base, engine
from app.models import associations, client, project, user  # noqa: F401 — registers all models
from app.routers import auth, clients, projects, users

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Nimap Project Management API",
    description="REST API for managing Users, Clients, and Projects with JWT authentication",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(clients.router)
app.include_router(projects.router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "Nimap API is running"}
