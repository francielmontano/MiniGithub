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
        owner_id: int
    ) -> Repository:

        repo = Repository(
            name = name,
            is_private = is_private,
            owner_id = owner_id
        )

        self.db.add(repo)
        await self.db.commit()
        await self.db.refresh(repo)

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
            
            query = Select(Repository).where(Repository.name.ilike(f"%{buscador}%")).limit(limit)
            
            result = await self.db.execute(query)
            
            return result.scalars().all()

    async def repo_list_me(self, owner_id) -> list[Repository]:
                
                query = Select(Repository).where(Repository.owner_id == owner_id)
                
                result = await self.db.execute(query)
                
                return result.scalars().all()

    async def get_by_id(
            self,
            repo_id: int
        ) -> Repository:
            
            query = Select(Repository).where(Repository.id == repo_id)
            
            result = await self.db.execute(query)
            
            return result.scalar_one_or_none()

    async def repo_list(self,limit = 10) -> list[Repository]:
            
            query = Select(Repository).limit(limit)
            
            result = await self.db.execute(query)
            
            return result.scalars().all()