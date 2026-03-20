from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# 🔥 Request Schema (Create Appointment)
class AppointmentCreate(BaseModel):
    patient: str = Field(..., min_length=1, example="user1")
    doctor: str = Field(..., min_length=1, example="Dr Ahuja")
    date: str = Field(..., example="tomorrow")
    time: str = Field(..., example="10:30 AM")


# 🔥 Response Schema
class AppointmentResponse(BaseModel):
    id: int
    patient: str
    doctor: str
    date: str
    time: str
    created_at: Optional[datetime]

    class Config:
        from_attributes = True   # 🔥 for SQLAlchemy (Pydantic v2)