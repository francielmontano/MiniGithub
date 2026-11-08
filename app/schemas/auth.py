from pydantic import BaseModel,EmailStr, Field


class RegisterRequest(BaseModel):
    name: str = Field(
        min_length=2, 
        max_length=50, 
        pattern=r"^[a-zA-Z0-9_]+$"
    )
    
    email: EmailStr
    
    password: str = Field(
        min_length=8,
    )
    
class LoginRequest(BaseModel):
    email: EmailStr
    password:str 

class UserDateResponse(BaseModel):
    id: int
    name: str = Field(
        min_length=2,
        max_lenght=50,
        pattern=r"^[a-zA-Z0-9_]+$"
    )
    email: EmailStr
    
    
class AuthSuccessResponse(BaseModel):
    status: str
    user: UserDateResponse