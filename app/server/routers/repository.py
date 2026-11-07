from ...database import get_db
from ...models import Repository, User
from ...repositories import RepoRepository
from ...schemas.repository import RepositoryCreate, RepositoryUpdate, RepositoryResponse
from sqlalchemy.ext.asyncio import AsyncSession
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

router_repo = APIRouter()

#endopint para crear un repositorio
@router_repo.post("",response_model=RepositoryResponse, status_code=status.HTTP_201_CREATED)
async def repo_create(data_repo:RepositoryCreate, db: AsyncSession = Depends(get_db)) -> Repository:

    repository = RepoRepository(db)

    return await create_repo(repository, data_repo)

#endopint para actualizar un repositorio
@router_repo.patch("/{repo_id}",response_model= RepositoryResponse, status_code=status.HTTP_200_OK)
async def repo_update(
    repo_id: int, data: RepositoryUpdate, db: AsyncSession = Depends(get_db)
) -> Repository:

    repositorie = RepoRepository(db)
    repo = await get_repo(repositorie, repo_id)

    if not repo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repository not found",
        )

    return await update_repo(repositorie, repo, data)

#endponit para buscar un repositorio por el nombre
@router_repo.get("/search",response_model=list[RepositoryResponse], status_code=status.HTTP_200_OK)
async def buscar_repo(
    q: str,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
) -> list[RepositoryResponse]:
    repositorie = RepoRepository(db)
    
    return  await repo_buscador(repositorie, q, limit)


#Endponit para ver mis repositorios(este endponit es experimental porque falta hacer la validacion automatica del usuario y solo te deja ver tus repos no los compartidos)
@router_repo.get("/me",response_model=list[RepositoryResponse], status_code=status.HTTP_200_OK)
async def repo_user(
        q: int,
        db: AsyncSession = Depends(get_db),
    ) -> list[RepositoryResponse]:
        repositorie = RepoRepository(db)
        
        return await user_repo(repositorie,q)

#endponit para borrar un repositorio
@router_repo.delete("/{repo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delte_user(repo_id: int, db: AsyncSession = Depends(get_db)) -> None:

    repositorie = RepoRepository(db)

    repo = await get_repo(repositorie, repo_id)

    if not repo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repository not found",
        )

    await delete_repo(repositorie,repo)


@router_repo.get("/list", response_model=list[RepositoryResponse], status_code=status.HTTP_200_OK)
async def list_all(db: AsyncSession = Depends(get_db), limit: int = 10) -> list[User]:

    repositorie = RepoRepository(db)

    return await list_all_repo(repositorie, limit)