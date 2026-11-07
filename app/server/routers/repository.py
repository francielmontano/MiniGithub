from ...database import get_db
from ...models import Repository, User
from ...repositories import RepoRepository
from ...schemas.repository import RepositoryCreate, RepositoryUpdate, RepositoryResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from fastapi import (
    APIRouter, 
    status, 
    Depends, 
    HTTPException
)

from ...services.repo_service import (
    create_repo,
    update_repo,
    user_repo,
    repo_buscador,
    delete_repo,
    get_repo,
    list_all_repo
)

router_repo = APIRouter(tags=["Repository"])

# Endpoint para crear un repositorio
@router_repo.post("", response_model=RepositoryResponse, status_code=status.HTTP_201_CREATED)
async def repo_create(data_repo: RepositoryCreate, db: AsyncSession = Depends(get_db)) -> Repository:
    repository = RepoRepository(db)
    try:
        return await create_repo(repository, data_repo)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

# Endpoint para actualizar un repositorio
@router_repo.patch("/{repo_id}", response_model=RepositoryResponse, status_code=status.HTTP_200_OK)
async def repo_update(
    repo_id: int, data: RepositoryUpdate, db: AsyncSession = Depends(get_db)
) -> Repository:
    repositorie = RepoRepository(db)
    
    try:
        repo = await get_repo(repositorie, repo_id)
        if not repo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Repositorio con ID {repo_id} no encontrado",
            )

        return await update_repo(repositorie, repo, data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar el repositorio."
        )

# Endpoint para buscar un repositorio por el nombre
@router_repo.get("/search", response_model=list[RepositoryResponse], status_code=status.HTTP_200_OK)
async def buscar_repo(
    q: str,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
) -> list[RepositoryResponse]:
    
    repositorie = RepoRepository(db)
    try:
        return await repo_buscador(repositorie, q, limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al realizar la búsqueda de repositorios."
        )

# Endpoint para ver mis repositorios
@router_repo.get("/repo-user", response_model=list[RepositoryResponse], status_code=status.HTTP_200_OK)
async def repo_user(
    user_id: int, 
    db: AsyncSession = Depends(get_db),
) -> list[RepositoryResponse]:
    repositorie = RepoRepository(db)
    try:
        repos = await user_repo(repositorie, user_id)
        return repos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener los repositorios del usuario."
        )

# Endpoint para borrar un repositorio
@router_repo.delete("/{repo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delte_user(repo_id: int, db: AsyncSession = Depends(get_db)) -> None:
    repositorie = RepoRepository(db)

    try:
        repo = await get_repo(repositorie, repo_id)
        if not repo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Repositorio con ID {repo_id} no encontrado",
            )

        await delete_repo(repositorie, repo)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar el repositorio."
        )

@router_repo.get("/list", response_model=list[RepositoryResponse], status_code=status.HTTP_200_OK)
async def list_all(db: AsyncSession = Depends(get_db), limit: int = 10) -> list[RepositoryResponse]:
    repositorie = RepoRepository(db)
    try:
        return await list_all_repo(repositorie, limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al listar los repositorios."
        )