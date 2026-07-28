from datetime import datetime 
from uuid import UUID 

from pydantic import BaseModel, ConfigDict, EmailStr 

class UserPreference(BaseModel):
    email: bool = True
    push: bool = True

class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    push_token: str | None = None
    preferences: UserPreference

class UserResponse(BaseModel):
    id: UUID
    name: str 
    email: EmailStr 
    push_token: str | None 
    preferences: UserPreference
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)