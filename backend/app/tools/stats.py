from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.appointment import Appointment


def get_appointments_stats(db: Session, date: str):
    """
    📊 Returns appointment statistics for a given date
    """

    try:
        # =========================
        # 🔥 Total Appointments
        # =========================
        total = db.query(func.count(Appointment.id)).filter(
            Appointment.date == date
        ).scalar()

        # =========================
        # 🔥 Doctor-wise Count
        # =========================
        doctor_stats = db.query(
            Appointment.doctor,
            func.count(Appointment.id).label("count")
        ).filter(
            Appointment.date == date
        ).group_by(Appointment.doctor).all()

        doctor_data = [
            {
                "doctor": d.doctor,
                "patients": d.count
            }
            for d in doctor_stats
        ]

        # =========================
        # 🔥 Time-slot usage
        # =========================
        time_stats = db.query(
            Appointment.time,
            func.count(Appointment.id).label("count")
        ).filter(
            Appointment.date == date
        ).group_by(Appointment.time).all()

        time_data = [
            {
                "time": t.time,
                "bookings": t.count
            }
            for t in time_stats
        ]

        # =========================
        # 🔥 Simple symptom estimation (demo logic)
        # =========================
        fever_cases = db.query(func.count(Appointment.id)).filter(
            Appointment.date == date,
            Appointment.patient.ilike("%fever%")
        ).scalar()

        # =========================
        # ✅ Final Response
        # =========================
        return {
            "status": "success",
            "date": date,
            "summary": {
                "total_appointments": total,
                "fever_cases": fever_cases
            },
            "doctor_stats": doctor_data,
            "time_stats": time_data
        }

    except Exception as e:
        print("❌ Stats Error:", str(e))

        return {
            "status": "error",
            "message": "Failed to fetch stats",
            "error": str(e)
        }