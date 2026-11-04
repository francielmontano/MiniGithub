from pydantic import BaseModel
from datetime import datetime

class RepositoryBase(BaseModel):

    name: str
    is_private: bool

class RepositoryCreate(BaseModel):
    owner_id: int

class RepositoryUpdate(RepositoryBase):
    name: str | None = None
    is_private: bool | None = None

class RepositoryResponse(RepositoryBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
            from_attributes = True