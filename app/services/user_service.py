import logging
import bcrypt

from ..models import User
from ..repositories import UserRespository
from ..schemas.user import CreateUser, UpdateUser

logger = logging.getLogger(__name__)

async def create_user(
    repositorie: UserRespository,
    data: CreateUser
) -> User:
    
    password_byte = data.password_hash.encode("utf-8")
    salt =  bcrypt.gensalt(rounds=12)
    
    pass_hash = bcrypt.hashpw(password_byte,salt)
    
    user = await repositorie.create(
        name = data.name,
        email = data.email,
        password_hash = pass_hash.decode('utf-8'),
        avatar_url = data.avatar_url,
        bio = data.bio,
        website_url = data.website_url
    )
    
    return user