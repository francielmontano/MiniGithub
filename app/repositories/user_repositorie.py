from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import Select
from ..models import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        name: str,
        email: str,
        password_hash: str,
        avatar_url: str = None,
        bio: str = None,
        website_url: str = None,
    ) -> User:

        user = User(
            name=name,
            email=email,
            password_hash=password_hash,
            avatar_url=avatar_url,
            bio=bio,
            website_url=website_url,
        )

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def update(self, user: User, updates: dict) -> User:

        for field, value in updates.items():
            setattr(user, field, value)

        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def delete(self, user: User) -> None:

        await self.db.delete(user)
        await self.db.commit()

    async def get_by_id(self, user_id: int) -> User:

        query = Select(User).where(User.id == user_id)

        result = await self.db.execute(query)

        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User:

        query = Select(User).where(User.email == email)

        result = await self.db.execute(query)

        return result.scalar_one_or_none()

    async def user_list(self, limit=10) -> list[User]:

        query = Select(User).limit(limit)

        result = await self.db.execute(query)

        return result.scalars().all()
