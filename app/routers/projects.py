from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.models.client import Client
from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectResponse
from app.schemas.user import UserBrief

router = APIRouter(prefix="/projects", tags=["Projects"])


def _build_project_response(project: Project) -> ProjectResponse:
    return ProjectResponse(
        id=project.id,
        project_name=project.project_name,
        created_at=project.created_at,
        client_name=project.client.client_name,
        users=[UserBrief.model_validate(u) for u in project.users],
    )


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    client = db.query(Client).filter(Client.id == project_data.client_id).first()
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

    users = db.query(User).filter(User.id.in_(project_data.users)).all()
    if len(users) != len(project_data.users):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more user IDs do not exist",
        )

    project = Project(project_name=project_data.project_name, client_id=client.id)
    project.users = users
    db.add(project)
    db.commit()
    db.refresh(project)
    return _build_project_response(project)


@router.get("/", response_model=List[ProjectResponse])
def list_my_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    projects = (
        db.query(Project)
        .join(Project.users)
        .filter(User.id == current_user.id)
        .all()
    )
    return [_build_project_response(p) for p in projects]


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    db.delete(project)
    db.commit()
