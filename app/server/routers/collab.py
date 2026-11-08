from ...database import get_db
from ...models import Repository_Collaborators
from ...repositories import Repo_Collab
from ...schemas.repository_collaborators import CollaboratorCreate, CollaboratorUpdate, CollaboratorResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from fastapi import (
    APIRouter, 
    status, 
    Depends, 
    HTTPException
)

from ...services.collab_service import (
    create_collab,
    update_collab,
    delete_collab,
    list_collab,
    get_collab
)

router_collab = APIRouter(tags=["Collab"])

# Endpoint para agregar un colaborador
@router_collab.post("", response_model=CollaboratorResponse, status_code=status.HTTP_201_CREATED)
async def collab_create(data_repo: CollaboratorCreate, db: AsyncSession = Depends(get_db)) -> Repository_Collaborators:
    repository = Repo_Collab(db)
    try:
        return await create_collab(repository, data_repo)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

# Endpoint para actualizar un collaborador
@router_collab.patch("/{repo_id}", response_model=CollaboratorResponse, status_code=status.HTTP_200_OK)
async def collab_update(
    repo_id: int, user_id:int, data: CollaboratorUpdate, db: AsyncSession = Depends(get_db)
) -> Repository_Collaborators:
    repositorie = Repo_Collab(db)
    
    try:
        collab = await get_collab(repositorie, repo_id, user_id)
        if not collab:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Repositorio con ID {repo_id} no encontrado",
            )

        return await update_collab(repositorie, collab, data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar el repositorio."
        )

# Endpoint para obtener todos los colaboradores de un repositorio
@router_collab.get("/list", response_model=list[CollaboratorResponse], status_code=status.HTTP_200_OK)
async def buscar_repo(
    repo_id: int,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
) -> list[CollaboratorResponse]:
    
    repositorie = Repo_Collab(db)
    try:
        return await list_collab(repositorie, repo_id, limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al realizar la búsqueda de repositorios."
        )

# Endpoint para borrar un collaborador
@router_collab.delete("/{repo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delte_user(repo_id: int,user_id:int, db: AsyncSession = Depends(get_db)) -> None:
    repositorie = Repo_Collab(db)

    try:
        repo = await get_collab(repositorie, repo_id, user_id)
        if not repo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Repositorio con ID {repo_id} no encontrado",
            )

        await delete_collab(repositorie, repo)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar el repositorio."
        )