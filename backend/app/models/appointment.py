from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.core.database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    patient = Column(String, nullable=False, index=True)

    doctor = Column(String, nullable=False, index=True)

    date = Column(String, nullable=False)   # can upgrade to Date later

    time = Column(String, nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )