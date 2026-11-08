from ..models import Repository_Collaborators
from ..repositories import Repo_Collab
from ..schemas.repository_collaborators import CollaboratorCreate, CollaboratorUpdate
from  pydantic import ValidationError

async def create_repo(
    repositorie: Repository_Collaborators,
    data: Repository_Collaborators,
)-> Repository_Collaborators:
    try:
        repo = await repositorie.create(
            repository_id = data.repository_id,
            user_id = data.user_id,
            role = data.role
        )
    except ValidationError as e:
            print("Error en la validacion de datos.")
            print(e.errors())
    return repo

async def update_repo(
    repositories: Repository_Collaborators,
    collab: Repository_Collaborators,
    data: CollaboratorUpdate
)-> Repository_Collaborators:
    if not data:
            return collab
        
    return await repositories.update(collab,data)

async def list_collab(
    repositories: Repository_Collaborators, 
    repo_id: int,
    limit: int
)-> list[Repository_Collaborators]:
    return await repositories.repository_collaborators_list(repo_id,limit)

async def delete_repo(
    repositorie: Repository_Collaborators,
    collab: Repository_Collaborators
) -> None:
    
    return await repositorie.delete(collab)