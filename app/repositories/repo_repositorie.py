from sqlalchemy.ext.asyncio import AsyncSession 
from fastapi import HTTPException
from sqlalchemy import Select
from ..models import Repository

class RepoRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        name: str,
        is_private: bool,
        owner_id: str
    ) -> Repository:

        repo = Repository(
            name = name,
            is_private = is_private,
            owner_id = owner_id
        )

        self.db.add(repo)
        await self.db.commit()
        await self.db.refresh()

        return repo

    async def update(
            self,
            repo: Repository,
            updates: dict
        ) -> Repository:
            
            for field, value in updates.items():
                setattr(repo,field,value)
                
            await self.db.commit()
            await self.db.refresh(repo)
            
            return repo

    async def delete(
            self,
            repo: Repository
        ) -> None:
            
            await self.db.delete(repo)
            await self.db.commit()

    async def repo_list_buscador(self, buscador: str, limit: int = 10) -> list[Repository]:
            
            query = Select(Repository).where(Repository.name == buscador).limit(limit)
            
            result = await self.db.execute(query)
            
            return result.scalars().all()

    async def repo_list(self, id_usuario) -> list[Repository]:
                
                query = Select(Repository).where(Repository.owner_id == id_usuario)
                
                result = await self.db.execute(query)
                
                return result.scalars().all()