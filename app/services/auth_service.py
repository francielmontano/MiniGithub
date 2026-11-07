from datetime import datetime, timedelta, timezone
import bcrypt, jwt
from ..server.configure import settings


async def verify_pass(plain_pass: str, hash_pass: str) -> bool:

    try:
        return bcrypt.checkpw(plain_pass.encode("utf-8"), hash_pass.encode("utf-8"))
    except Exception:
        return False


async def generate_token(user_id: str, email: str) -> str:

    expired = datetime.now(timezone.utc) + timedelta(minutes=settings.acces_token_time)

    payload = {"sub": str(user_id), "email": email, "exp": expired}

    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
