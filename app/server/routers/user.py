from ...database import get_db
from ...models import User
from ...repositories import UserRepository
from ...schemas.user import CreateUser, UpdateUser, ResponseUser
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import (
    APIRouter, 
    status, 
    Depends, 
    HTTPException
    )

from ...services.user_service import (
    get_user_by_email,
    create_user,
    update_user,
    delete_user,
    list_user,
    get_user,
)

router_user = APIRouter(tags=["Users"])


@router_user.post("", response_model=ResponseUser, status_code=status.HTTP_201_CREATED)
async def user_create(user_data: CreateUser, db: AsyncSession = Depends(get_db)) -> User:

    repository = UserRepository(db)

    return await create_user(repository, user_data)


@router_user.get("", response_model=list[ResponseUser], status_code=status.HTTP_200_OK)
async def list_all(db: AsyncSession = Depends(get_db), limit: int = 10) -> list[User]:

    repositorie = UserRepository(db)

    return await list_user(repositorie, limit)


@router_user.get(
    "/{user_id}", response_model=ResponseUser, status_code=status.HTTP_200_OK
)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)) -> User:

    repositorie = UserRepository(db)
    user = await get_user(repositorie, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user

@router_user.get("/email/{email}",response_model=ResponseUser,status_code=status.HTTP_200_OK)
async def get_email(email:str,db: AsyncSession = Depends(get_db)) -> User:

    repositorie = UserRepository(db)
    user = await get_user_by_email(repositorie,email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
        
    return user

@router_user.patch(
    "/{user_id}", response_model=ResponseUser, status_code=status.HTTP_200_OK
)
async def user_update(
    user_id: int, data: UpdateUser, db: AsyncSession = Depends(get_db)
) -> User:

    repositorie = UserRepository(db)
    user = await get_user(repositorie, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return await update_user(repositorie, user, data)


@router_user.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delte_user(user_id: int, db: AsyncSession = Depends(get_db)) -> None:

    repositorie = UserRepository(db)

    user = await get_user(repositorie, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    await delete_user(repositorie,user)
