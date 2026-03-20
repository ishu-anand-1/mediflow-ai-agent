from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.schemas.domain import DoctorResponse, AvailabilityUpdate, StatusUpdate
from app.models.domain import Doctor

router = APIRouter()

@router.post("/status")
async def update_status(req: StatusUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Doctor).filter(Doctor.id == req.doctor_id))
    doc = result.scalars().first()
    if not doc:
        raise HTTPException(status_code=404, detail="Doctor not found")
    doc.is_active = req.is_active
    await db.commit()
    return {"message": f"Status updated to {'ON' if doc.is_active else 'OFF'}", "is_active": doc.is_active}

@router.get("", response_model=List[DoctorResponse])
async def get_doctors(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Doctor))
    return result.scalars().all()

@router.post("/availability")
async def update_availability(req: AvailabilityUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Doctor).filter(Doctor.id == req.doctor_id))
    doc = result.scalars().first()
    if not doc:
        raise HTTPException(status_code=404, detail="Doctor not found")
        
    avail = dict(doc.available_slots) if doc.available_slots else {}
    avail[req.date] = req.slots
    doc.available_slots = avail
    await db.commit()
    return {"message": "Availability updated"}

@router.get("/{doctor_id}/availability/{date_str}")
async def get_availability(doctor_id: int, date_str: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Doctor).filter(Doctor.id == doctor_id))
    doc = result.scalars().first()
    if not doc:
        raise HTTPException(status_code=404, detail="Doctor not found")
        
    avail = doc.available_slots or {}
    return {"date": date_str, "slots": avail.get(date_str, [])}
