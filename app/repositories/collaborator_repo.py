from sqlalchemy.ext.asyncio import AsyncSession 
from fastapi import HTTPException
from sqlalchemy import Select
from ..models import Repository_Collaborators

class Repo_Collab:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def create(
        self,
        repository_id: int,
        user_id: int,
        role: str
    )-> Repository_Collaborators:
        collab = Repository_Collaborators(
            repository_id = repository_id,
            user_id = user_id,
            role = role
        )
        self.db.add(collab)
        await self.db.commit()
        await self.db.refresh(collab)

        return collab


    async def update(
        self,
        collab: Repository_Collaborators,
        updates: str
    ) -> Repository_Collaborators:

        await self.db.commit()
        await self.db.refresh(collab)

        return collab


    async def delete(
            self,
            collab: Repository_Collaborators
        ) -> None:
            
            await self.db.delete(collab)
            await self.db.commit()

    async def repository_collaborators_list(self, repository_id: int, limit: int = 10) -> list[Repository_Collaborators]:
        query = (
            Select(Repository_Collaborators).where(Repository_Collaborators.repository_id == repository_id).limit(limit)
        )

        result = await self.db.execute(query)

        return result.scalars().all()