from pydantic import Field, BaseModel, ConfigDict

class BaseCollaborator(BaseModel):
    role: str = Field(
        default="wirte",
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
    role: str = Field(..., max_length=20)

class CollaboratorResponse(BaseCollaborator):
    repository_id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)