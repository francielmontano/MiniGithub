from pydantic import Field, BaseModel, ConfigDict
from typing import Literal

class BaseCollaborator(BaseModel):
    role: Literal["collaborator", "visitant", "admin"] = Field(
        default="collaborator",
        max_length=20,
        description="Nivel de permiso del colaborador"
    )

class CollaboratorCreate(BaseCollaborator):
    repository_id: int = Field(
        gt=0,
        description = "Id del repositorio"
    )

    user_id: int = Field(
        gt = 0,
        description="Id del usuario que va a colaborar"
    )

class CollaboratorUpdate(BaseCollaborator):
    role: Literal["collaborator", "visitant", "admin"] = Field(..., description="Rol del colaborador en el repositorio")

class CollaboratorResponse(BaseCollaborator):
    repository_id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)