from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.core.database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False, index=True)

    specialization = Column(String, nullable=False, index=True)

    location = Column(String, nullable=True, index=True)  # 🔥 for nearby search

    email = Column(String, nullable=True, unique=True)    # 🔥 unique for safety

    availability = Column(String, nullable=True)  
    # Example: "10:00 AM,11:30 AM,2:00 PM"

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )