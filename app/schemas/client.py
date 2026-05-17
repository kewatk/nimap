from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.schemas.project import ProjectBrief


class ClientCreate(BaseModel):
    client_name: str


class ClientUpdate(BaseModel):
    client_name: Optional[str] = None


class ClientResponse(BaseModel):
    id: int
    client_name: str
    created_at: datetime
    created_by: str

    model_config = {"from_attributes": True}


class ClientDetailResponse(BaseModel):
    id: int
    client_name: str
    created_at: datetime
    created_by: str
    projects: List[ProjectBrief] = []

    model_config = {"from_attributes": True}
