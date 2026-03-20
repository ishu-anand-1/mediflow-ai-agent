from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.appointment import Appointment

router = APIRouter()


# 🔥 Get all appointments
@router.get("/appointments")
def get_all_appointments(db: Session = Depends(get_db)):
    try:
        appointments = db.query(Appointment).all()

        return {
            "status": "success",
            "count": len(appointments),
            "data": [
                {
                    "id": a.id,
                    "patient": a.patient,
                    "doctor": a.doctor,
                    "date": a.date,
                    "time": a.time
                }
                for a in appointments
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 🔥 Create appointment manually
@router.post("/appointments")
def create_appointment(
    patient: str,
    doctor: str,
    date: str,
    time: str,
    db: Session = Depends(get_db)
):
    try:
        # 🔥 Check if slot already booked
        existing = db.query(Appointment).filter(
            Appointment.doctor == doctor,
            Appointment.date == date,
            Appointment.time == time
        ).first()

        if existing:
            return {
                "status": "failed",
                "message": f"❌ Slot {time} already booked for {doctor}"
            }

        appointment = Appointment(
            patient=patient,
            doctor=doctor,
            date=date,
            time=time
        )

        db.add(appointment)
        db.commit()
        db.refresh(appointment)

        return {
            "status": "success",
            "message": "✅ Appointment created",
            "data": {
                "id": appointment.id,
                "patient": patient,
                "doctor": doctor,
                "date": date,
                "time": time
            }
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))