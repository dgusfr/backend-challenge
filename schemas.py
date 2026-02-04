from pydantic import BaseModel, EmailStr
from typing import Optional


class RoleResponse(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    role_id: int
    password: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: RoleResponse

    class Config:
        from_attributes = True
