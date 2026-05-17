from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.schemas.user import UserBrief


class ProjectCreate(BaseModel):
    project_name: str
    client_id: int
    users: List[int]


class ProjectBrief(BaseModel):
    id: int
    project_name: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ProjectResponse(BaseModel):
    id: int
    project_name: str
    created_at: datetime
    client_name: str
    users: List[UserBrief] = []

    model_config = {"from_attributes": True}
