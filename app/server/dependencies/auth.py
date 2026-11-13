import jwt
from typing import Optional
from fastapi import Cookie, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ...services.user_service import get_user
from ...repositories.user_repositorie import UserRepository
from ...server.configure import settings
from ...database import get_db
from ...models import User


async def get_current_user(
    access_token: Optional[str] = Cookie(None), db: AsyncSession = Depends(get_db)
) -> User:
    
    repositorie = UserRepository(db)
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Non-existent session."
        )
    try:

        payload = jwt.decode(
            access_token, settings.secret_key, algorithms=[settings.algorithm]
        )

        user_id = payload["user"]["id"]

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Your session has expired. Please log in again.",
            )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tu sesión ha expirado. Vuelve a iniciar sesión.",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de sesión corrupto o dañado.",
        )

    user = get_user(repositorie, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user associated with this session no longer exists.",
        )

    return user
