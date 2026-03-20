from sqlalchemy.orm import Session
from app.models.appointment import Appointment


# 🔥 Default available slots (Doctor working hours)
DEFAULT_SLOTS = ["10:30 AM", "11:30 AM", "3:00 PM", "5:00 PM"]


def check_doctor_availability(db: Session, doctor: str, date: str):
    try:
        # 🔥 Get booked slots from DB
        booked_appointments = db.query(Appointment).filter(
            Appointment.doctor == doctor,
            Appointment.date == date
        ).all()

        booked_slots = [appt.time for appt in booked_appointments]

        # 🔥 Remove booked slots
        available_slots = [
            slot for slot in DEFAULT_SLOTS if slot not in booked_slots
        ]

        return available_slots

    except Exception as e:
        print("❌ Availability Error:", str(e))
        return []