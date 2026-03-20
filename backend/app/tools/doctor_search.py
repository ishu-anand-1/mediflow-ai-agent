from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.doctor import Doctor


def find_doctors_by_specialization(
    db: Session,
    specialization: str,
    location: str = None
):
    """
    🔍 Find doctors by specialization (and optional location)
    """

    try:
        # =========================
        # 🔍 Base Query
        # =========================
        query = db.query(Doctor).filter(
            Doctor.specialization.ilike(f"%{specialization}%")
        )

        # =========================
        # 📍 Location Filter
        # =========================
        if location:
            query = query.filter(
                Doctor.location.ilike(f"%{location}%")
            )

        doctors = query.all()

        # =========================
        # 🔥 Ranking (Exact match first)
        # =========================
        doctors_sorted = sorted(
            doctors,
            key=lambda d: (
                0 if d.specialization.lower() == specialization.lower() else 1
            )
        )

        # =========================
        # 📦 Format Response
        # =========================
        result = [
            {
                "id": d.id,
                "name": d.name,
                "specialization": d.specialization,
                "location": d.location,
                "email": d.email
            }
            for d in doctors_sorted
        ]

        return result

    except Exception as e:
        print("❌ Doctor Search Error:", str(e))

        return []