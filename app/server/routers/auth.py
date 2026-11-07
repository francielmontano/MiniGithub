from ...models import User
from ...repositories import UserRepository
from ...schemas.user import CreateUser, UpdateUser, ResponseUser
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import (
    APIRouter, 
    status, 
    Depends, 
    HTTPException,
    Response
    )

from ...services.user_service import (
    get_user_by_email,
    create_user,
    update_user,
    delete_user,
    list_user,
    get_user,
)

router_auth = APIRouter(
    tags= ["Auth"]
)

@router_auth.post("/login",status_code=status.HTTP_200_OK)
async def login(
    respose: Response
):
    pass