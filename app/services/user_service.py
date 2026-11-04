import bcrypt

from ..models import User
from ..repositories import UserRepository
from ..schemas.user import CreateUser, UpdateUser
from  pydantic import ValidationError

async def create_user(
    repositorie: UserRepository,
    data: CreateUser
) -> User:
    
    password_byte = data.password_hash.encode("utf-8")
    salt =  bcrypt.gensalt(rounds=12)
    
    pass_hash = bcrypt.hashpw(password_byte,salt)
    
    try:
        user = await repositorie.create(
            name = data.name,
            email = data.email,
            password_hash = pass_hash.decode('utf-8'),
            avatar_url = data.avatar_url,
            bio = data.bio,
            website_url = f"/{data.name}"
        ) 
    except ValidationError as e:
        print("Error en la validacion de datos.")
        print(e.errors())
        

    
    return user

async def get_user(
    repositorie: UserRepository,
    user_id: int
) -> User:
    
    return await repositorie.get_by_id(user_id)

async def list_user(
    repositorie: UserRepository,
    limit: int = 10
) -> list[User]:
    
    return await repositorie.user_list(limit)

async def update_user(
    repositorie: UserRepository,
    user: User,
    data: UpdateUser
) -> User:
    
    update = data.model_dump(
        exclude_unset=True
    )
    
    if not update:
        return user
    
    return await repositorie.update(user,update)

async def delete_user(
    repositorie: UserRepository,
    user: User
) -> None:
    
    return await repositorie.delete(user)