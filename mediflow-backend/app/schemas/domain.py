from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import date, time

class DoctorBase(BaseModel):
    name: str
    email: str
    specialization: str
    experience: Optional[str] = None
    education: Optional[str] = None
    location: str
    available_slots: Optional[Dict[str, List[str]]] = {}
    default_slots: Optional[List[str]] = ["09:00", "10:00", "16:00", "17:00"]
    is_active: bool = True

class DoctorCreate(DoctorBase):
    pass

class DoctorResponse(DoctorBase):
    id: int
    class Config:
        from_attributes = True

class PatientBase(BaseModel):
    name: str
    email: str

class PatientResponse(PatientBase):
    id: int
    class Config:
        from_attributes = True

class AppointmentBase(BaseModel):
    doctor_id: int
    patient_id: int
    date: date
    time: time
    disease: str

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentResponse(AppointmentBase):
    id: int
    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str
    session_id: str

class ChatResponse(BaseModel):
    message: str
    data: Optional[dict] = None

class BookRequest(BaseModel):
    patient_name: str
    doctor_id: int
    time: str
    date: str
    disease: str

class AvailabilityUpdate(BaseModel):
    doctor_id: int
    date: str
    slots: List[str]

class StatusUpdate(BaseModel):
    doctor_id: int
    is_active: bool
