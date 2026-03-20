from sqlalchemy.orm import Session
from app.models.appointment import Appointment
from app.services.calendar_service import create_calendar_event
from app.tools.email import send_email


def book_appointment(
    db: Session,
    patient: str,
    doctor: str,
    date: str,
    time: str
):
    """
    📅 Books an appointment safely
    """

    try:
        # =========================
        # 🔍 Check duplicate booking
        # =========================
        existing = db.query(Appointment).filter(
            Appointment.doctor == doctor,
            Appointment.date == date,
            Appointment.time == time
        ).first()

        if existing:
            return {
                "status": "failed",
                "message": f"❌ {doctor} already booked at {time}",
                "suggestion": "Try another time slot"
            }

        # =========================
        # 🆕 Create appointment
        # =========================
        appointment = Appointment(
            patient=patient,
            doctor=doctor,
            date=date,
            time=time
        )

        db.add(appointment)
        db.commit()
        db.refresh(appointment)

        # =========================
        # 📅 Calendar Integration
        # =========================
        calendar_event = create_calendar_event(doctor, date, time)

        # =========================
        # 📧 Email Notification
        # =========================
        send_email(
            email=f"{patient}@mail.com",  # demo email
            message=f"Appointment confirmed with {doctor} at {time}"
        )

        # =========================
        # ✅ Final Response
        # =========================
        return {
            "status": "confirmed",
            "message": f"✅ Appointment confirmed with {doctor} at {time}",
            "data": {
                "id": appointment.id,
                "patient": patient,
                "doctor": doctor,
                "date": date,
                "time": time
            },
            "calendar": calendar_event
        }

    except Exception as e:
        # 🔥 rollback on failure
        db.rollback()

        return {
            "status": "error",
            "message": "❌ Booking failed",
            "error": str(e)
        }