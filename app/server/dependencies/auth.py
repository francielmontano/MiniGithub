import jwt
from typing import Optional
from fastapi import Cookie, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ...services.user_service import get_user
from ...repositories.user_repositorie import UserRepository
from ...server.configure import settings
from ...database import get_db
from ...models import User


async def get_current_payload(access_token: Optional[str] = Cookie(None)) -> dict:
    """Funcion que obtiene y validad los datos de usuario del jwt de la cookie de seguridad"""
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Non-existent session."
        )

    try:
        payload = jwt.decode(
            access_token, settings.secret_key, algorithms=[settings.algorithm]
        )
        if not payload.get("user", {}).get("id"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload.",
            )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your session has expired. Please log in again.",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Corrupt or damaged session token.",
        )


async def get_current_user(
    payload: dict = Depends(get_current_payload), db: AsyncSession = Depends(get_db)
) -> User:
    repositorie = UserRepository(db)
    user_id = payload["user"]["id"]
    
    user = await get_user(repositorie,user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user associated with this session no longer exists.",
        )
    return user 