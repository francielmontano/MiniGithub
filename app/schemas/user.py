from pydantic import Field, EmailStr, HttpUrl, BaseModel, FilePath, ConfigDict

from datetime import datetime


class UserBase(BaseModel):

    name: str = Field(
        min_length=2, 
        max_length=50, 
        pattern=r"^[a-zA-Z0-9_]+$"
    )
    
    email: EmailStr = Field(
        description="Email del usuario."
    
    )
    
    avatar_url: FilePath | None = Field(
        default= None,
        description= "Ruta de foto de perfil del usuario."
    )
    
    bio: str | None = Field(
        default=None,
        description="Descripcion del perfil del usuario."
    )

    model_config = ConfigDict(
        str_strip_whitespace=True
    )
class CreateUser(UserBase):
    password_hash: str = Field(
        min_length=8, 
        exclude=True
    )


class UpdateUser(UserBase):
    name: str | None = Field(
        default=None, 
        min_length=2, 
        max_length=50, pattern=r"^[a-zA-Z0-9_]+$"
    )
    
    email: EmailStr | None = Field(
        default=None, 
        description="Email del usuario."
    )
    
    avatar_url: FilePath | None = Field(
        default=None, 
        description="Ruta del foto de perfil del usuario"
    )
    
    password_hash: str | None = Field(
        default= None,
        min_length=8, 
        exclude=True
    )
    
    bio: str | None = Field(
        default=None, 
        description="Descripcion del perfil del usuario."
    )


    model_config = ConfigDict(
        extra="forbid", 
        str_strip_whitespace=True
    )


class ResponseUser(UserBase):
    id: int
    create_at: datetime
    update_at: datetime

    model_config = ConfigDict(
        from_attributes= True,   
        str_strip_whitespace=True
    )