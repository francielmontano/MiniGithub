from pydantic import Field, EmailStr, HttpUrl, BaseModel, FilePath, ConfigDict

from datetime import datetime

class UserBase(BaseModel):

    name: str
    email: EmailStr
    avatar_url: FilePath | None = None
    bio: str | None = None
    website_url: HttpUrl | None = None


class CreateUser(UserBase):
    password_hash: str

    model_config = ConfigDict(str_strip_whitespace=True)

class UpdateUser(UserBase):
    username: str | None = None
    email: EmailStr | None = None 
    avatar_url: FilePath | None = None
    password_hash: str | None = None
    bio: str | None = None
    website_url: HttpUrl | None = None
    
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True
    )
    
class ResponseUser(UserBase):
    id: int
    create_at: datetime
    update_at: datetime

    class config:
        
        from_attributes = True 
