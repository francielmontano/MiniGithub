from pydantic import BaseModel, ConfigDict
from datetime import datetime

class RepositoryBase(BaseModel):

    name: str
    is_private: bool

class RepositoryCreate(RepositoryBase):
    owner_id: int

class RepositoryUpdate(RepositoryBase):
    name: str | None = None
    is_private: bool | None = None

class RepositoryResponse(RepositoryBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
            from_attributes= True,   
            str_strip_whitespace=True
        )