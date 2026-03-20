from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from datetime import datetime
from app.core.database import get_db
from app.schemas.domain import AppointmentResponse, BookRequest
from app.models.domain import Appointment, Doctor, Patient
import json

router = APIRouter()

@router.get("", response_model=List[AppointmentResponse])
async def list_appointments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Appointment))
    return result.scalars().all()

@router.post("/book")
async def book_appointment_direct(req: BookRequest, db: AsyncSession = Depends(get_db)):
    p_res = await db.execute(select(Patient).filter(Patient.name == req.patient_name))
    patient = p_res.scalars().first()
    if not patient:
        patient = Patient(name=req.patient_name, email=f"{req.patient_name.lower().replace(' ','')}@demo.com")
        db.add(patient)
        await db.flush()
        
    d_res = await db.execute(select(Doctor).filter(Doctor.id == req.doctor_id))
    doc = d_res.scalars().first()
    if not doc:
        raise HTTPException(status_code=404, detail="Doctor not found")
        
    slots = doc.available_slots.get(req.date, [])
    if req.time not in slots:
        raise HTTPException(status_code=400, detail="Slot not available")
        
    appt = Appointment(
        doctor_id=req.doctor_id,
        patient_id=patient.id,
        date=datetime.strptime(req.date, "%Y-%m-%d").date(),
        time=datetime.strptime(req.time, "%H:%M").time(),
        disease=req.disease
    )
    db.add(appt)
    
    new_slots = [s for s in slots if s != req.time]
    current_avail = dict(doc.available_slots)
    current_avail[req.date] = new_slots
    doc.available_slots = current_avail
    await db.commit()
    
    return {"message": "Your appointment is confirmed at " + req.time, "data": {"appointment_id": appt.id}}
