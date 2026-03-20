from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# 🔥 Request Schema (Create User)
class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, example="Ishu")
    email: EmailStr = Field(..., example="ishu@gmail.com")
    phone: Optional[str] = Field(None, example="9876543210")


# 🔥 Response Schema
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: Optional[str]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True   # 🔥 for SQLAlchemy (Pydantic v2)