from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.models.client import Client
from app.models.user import User
from app.schemas.client import ClientCreate, ClientDetailResponse, ClientResponse, ClientUpdate
from app.schemas.project import ProjectBrief

router = APIRouter(prefix="/clients", tags=["Clients"])


def _build_client_response(client: Client) -> ClientResponse:
    return ClientResponse(
        id=client.id,
        client_name=client.client_name,
        created_at=client.created_at,
        created_by=client.creator.name,
    )


def _build_client_detail_response(client: Client) -> ClientDetailResponse:
    return ClientDetailResponse(
        id=client.id,
        client_name=client.client_name,
        created_at=client.created_at,
        created_by=client.creator.name,
        projects=[ProjectBrief.model_validate(p) for p in client.projects],
    )


@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(
    client_data: ClientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    client = Client(client_name=client_data.client_name, created_by_id=current_user.id)
    db.add(client)
    db.commit()
    db.refresh(client)
    return _build_client_response(client)


@router.get("/", response_model=List[ClientResponse])
def list_clients(db: Session = Depends(get_db)):
    clients = db.query(Client).all()
    return [_build_client_response(c) for c in clients]


@router.get("/{client_id}", response_model=ClientDetailResponse)
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    return _build_client_detail_response(client)


@router.put("/{client_id}", response_model=ClientResponse)
@router.patch("/{client_id}", response_model=ClientResponse)
def update_client(
    client_id: int,
    client_data: ClientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    if client_data.client_name is not None:
        client.client_name = client_data.client_name
    db.commit()
    db.refresh(client)
    return _build_client_response(client)


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    db.delete(client)
    db.commit()
