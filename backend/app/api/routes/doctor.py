from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.appointment import Appointment

router = APIRouter()


# 🔥 Get all appointments of a doctor
@router.get("/doctor/appointments")
def get_doctor_appointments(doctor: str, db: Session = Depends(get_db)):
    try:
        appointments = db.query(Appointment).filter(
            Appointment.doctor == doctor
        ).all()

        return {
            "status": "success",
            "doctor": doctor,
            "count": len(appointments),
            "data": [
                {
                    "id": a.id,
                    "patient": a.patient,
                    "date": a.date,
                    "time": a.time
                }
                for a in appointments
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 🔥 Doctor stats (with optional date filter)
@router.get("/doctor/stats")
def get_stats(date: str = None, db: Session = Depends(get_db)):
    try:
        query = db.query(Appointment)

        if date:
            query = query.filter(Appointment.date == date)

        appointments = query.all()
        total = len(appointments)

        # 🔥 Example insight (basic AI-style)
        fever_cases = len([
            a for a in appointments if "fever" in a.patient.lower()
        ])

        return {
            "status": "success",
            "date": date if date else "all",
            "total_patients": total,
            "fever_cases": fever_cases,
            "message": f"You handled {total} patients. "
                       f"{fever_cases} had fever cases."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))