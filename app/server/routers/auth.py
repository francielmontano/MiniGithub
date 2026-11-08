from ...models import User
from ..configure import settings
from ...database import get_db
from ...repositories import UserRepository
from ...schemas.user import CreateUser
from ...schemas.auth import AuthSuccessResponse, LoginRequest
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
    get_user,
)

from ...services.auth_service import (
    verify_pass,
    generate_token
)

router_auth = APIRouter(
    tags= ["Auth"]
)

@router_auth.post("/register",status_code=status.HTTP_200_OK)
async def login(payload:CreateUser,db: AsyncSession = Depends(get_db)):
    repositorie = UserRepository(db)
    user = await get_user_by_email(repositorie,payload.email)

    if user:
        raise HTTPException(
            status_code= status.HTTP_409_CONFLICT,
            detail= "This email is registered."
        )

    new_user = await create_user(repositorie,payload)
    
    token = generate_token(new_user.id,new_user.email)
    
    return {
        "status": "success",
        "token": str(token),
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
        }
    }
   
    
@router_auth.post("/login",response_model=AuthSuccessResponse,status_code=status.HTTP_200_OK)
async def login(payload: LoginRequest,response: Response,db: AsyncSession = Depends(get_db)):
    respositorie = UserRepository(db)
    user = await get_user_by_email(respositorie,payload.email)
    
    if not user:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Invalid user or password"
        )
    
    if not await verify_pass(payload.password,user.password_hash):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Invalid user or password"
        )
    
    token = generate_token(user.id,user.email)
    
    response.set_cookie(
        key = "access_token",
        value = token,
        httponly= True,
        secure = False if settings.enviroment == "development" else True,
        samesite = "lax",
        max_age = str(settings.acces_token_time * 60)
    )
    
    return {
        "status": "success",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        }
    }
    
    
    
@router_auth.post("logout")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"status": "success", "message": "Sesión cerrada"}