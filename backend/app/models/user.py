from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False, index=True)

    email = Column(String, unique=True, nullable=False, index=True)

    phone = Column(String, nullable=True)   # 🔥 for WhatsApp/SMS

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )