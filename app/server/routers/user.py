from ...database import get_db
from ...models import User
from ...repositories import UserRespository
from fastapi import APIRouter, status, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas.user import CreateUser, UpdateUser, ResponseUser

from ...services.user_service import (
    create_user
)

router_user = APIRouter()


@router_user.post(
    "", response_model=ResponseUser, status_code=status.HTTP_201_CREATED
)
async def user_create(user_data: CreateUser, db: AsyncSession = Depends(get_db)):

    repository = UserRespository(db)
   
    return await create_user(repository,user_data)


@router_user.get(
    '',
    response_model= list[ResponseUser],
    status_code=status.HTTP_200_OK
) 
async def list_all(db: AsyncSession = Depends(get_db), limit:int = 10):
    
    repository = UserRespository(db)
    
    return await repository.user_list(limit)


@router_user.get(
    "/{user_id}", response_model=ResponseUser, status_code=status.HTTP_200_OK
)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):

   
    repositorie = UserRespository(db)
    
    return await repositorie.get_by_id(user_id)


@router_user.delete("/{user_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delte_user(user_id: int,db: AsyncSession = Depends(get_db)):
    
    repository = UserRespository(db)
    
    user = repository.get_by_id(user_id)
    
    repository.delete(user)
    
    