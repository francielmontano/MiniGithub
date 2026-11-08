from pydantic import Field, BaseModel, ConfigDict
from datetime import datetime

class RepositoryBase(BaseModel):
    name: str = Field(
        min_length=2, 
        max_length=50, 
        pattern=r"^[a-zA-Z0-9_]+$",
        description="Nombre único del repositorio (letras, números y guiones bajos)"
    )
    is_private: bool = Field(
        default=False,
        description="Define si el repositorio es privado o público"
    )

class RepositoryCreate(RepositoryBase):
    owner_id: int = Field(
        gt=0, 
        description="ID del propietario, debe ser un entero positivo"
    )

class RepositoryUpdate(RepositoryBase):
    name: str | None = Field(
        default=None, 
        min_length=2, 
        max_length=50, 
        pattern=r"^[a-zA-Z0-9_]+$"
    )
    is_private: bool | None = None

class RepositoryResponse(RepositoryBase):
    id: int = Field(gt=0)
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,   
        str_strip_whitespace=True
    )