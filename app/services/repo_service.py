from ..models import Repository
from ..repositories import RepoRepository
from ..schemas.repository import RepositoryCreate, RepositoryUpdate
from  pydantic import ValidationError

async def create_repo(
    repositorie: RepoRepository,
    data: RepositoryCreate
)-> Repository:
    try:
        repo = await repositorie.create(
            name = data.name,
            is_private= data.is_private,
            owner_id = data.owner_id
        )
    except ValidationError as e:
            print("Error en la validacion de datos.")
            print(e.errors())
    return repo

async def update_repo(
    repositories: RepoRepository,
    repo: Repository,
    data: RepositoryUpdate
)-> Repository:
    update = data.model_dump(
            exclude_unset=True
        )
    if not update:
            return repo
        
    return await repositories.update(repo,update)

async def user_repo(
    repositories: RepoRepository, 
    owner_id: int
)-> list[Repository]:
    return await repositories.repo_list(owner_id)

async def repo_buscador(
    repositories: RepoRepository,
    name_repo: str,
    limite = 10
)-> list[Repository]:
    return await repositories.repo_list_buscador(name_repo, limite)

async def delete_repo(
    repositorie: RepoRepository,
    repo: RepoRepository
) -> None:
    
    return await repositorie.delete(repo)