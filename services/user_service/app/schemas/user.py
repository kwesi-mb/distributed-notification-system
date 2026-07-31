# from datetime import datetime 
# from uuid import UUID 

# from pydantic import BaseModel, ConfigDict, EmailStr 

# class UserPreference(BaseModel):
#     email: bool = True
#     push: bool = True

# class CreateUserRequest(BaseModel):
#     name: str
#     email: EmailStr
#     password: str
#     push_token: str | None = None
#     preferences: UserPreference

# class UserResponse(BaseModel):
#     id: UUID
#     name: str 
#     email: EmailStr 
#     push_token: str | None 
#     preferences: UserPreference
#     created_at: datetime

#     model_config = ConfigDict(from_attributes=True)


from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserPreference(BaseModel):
    email: bool = True
    push: bool = True

class CreateUserRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
    )

    push_token: str | None = None

    preferences: UserPreference = UserPreference()

class UserResponse(BaseModel):
    id: UUID

    name: str

    email: EmailStr

    push_token: str | None

    preferences: UserPreference

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )

class PaginationMeta(BaseModel):
    total: int
    limit: int
    page: int
    total_pages: int
    has_next: bool
    has_previous: bool

class UpdateUserRequest(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)

    email: EmailStr | None = None 

    password: str | None = Field(default=None, min_length=8)

    push_token: str | None = None

    email_enabled: bool | None = None

    push_enabled: bool | None = None

    model_config = ConfigDict(
        extra="forbid", 
    )