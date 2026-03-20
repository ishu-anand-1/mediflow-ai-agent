from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from app.api.routes import chat, doctor, appointments
from app.core.database import engine, Base, AsyncSessionLocal
from app.models.domain import Patient, Doctor
import contextlib
import datetime

async def seed_db():
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(Patient).filter(Patient.email == "patient@demo.com"))
        patient = res.scalars().first()
        if not patient:
            patient = Patient(name="Demo Patient", email="patient@demo.com")
            session.add(patient)
            
        res = await session.execute(select(Doctor))
        existing_docs = res.scalars().all()
        if len(existing_docs) < 5:
            today_str = datetime.datetime.now().strftime("%Y-%m-%d")
            docs_data = [
                Doctor(name="Dr. Sarah Johnson", email="sarah@demo.com", specialization="Cardiologist", experience="10 Years", education="MD Cardiology", location="Downtown", default_slots=["09:00", "10:00"], available_slots={today_str: ["09:00", "10:30"]}),
                Doctor(name="Dr. Marcus Wei", email="marcus@demo.com", specialization="Gastroenterologist", experience="15 Years", education="MD Gastroenterology", location="Uptown", default_slots=["11:00", "14:00"], available_slots={today_str: ["11:00", "14:00"]}),
                Doctor(name="Dr. Emily Chen", email="emily@demo.com", specialization="Dermatologist", experience="8 Years", education="MD Dermatology", location="Westside", default_slots=["09:00", "15:00"], available_slots={today_str: ["09:00", "15:00"]}),
                Doctor(name="Dr. James Wilson", email="james@demo.com", specialization="General Physician", experience="20 Years", education="MBBS", location="Downtown", default_slots=["10:00", "16:00"], available_slots={today_str: ["10:00", "16:00"]}),
                Doctor(name="Dr. Priya Patel", email="priya@demo.com", specialization="Oncologist", experience="12 Years", education="MD Oncology", location="Eastside", default_slots=["13:00", "14:00"], available_slots={today_str: ["13:00", "14:00"]})
            ]
            for d in docs_data:
                existing = await session.execute(select(Doctor).filter(Doctor.email == d.email))
                if not existing.scalars().first():
                    session.add(d)
            
        await session.commit()

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    # Safe init for dev (drops old incompatible schemas if they existed? no, create_all does not alter or re-create.)
    async with engine.begin() as conn:
        # In a real scenario Alembic is used. For this single-shot demo iteration, we'll try create_all. 
        # Note: If schema changed drastically, this may not apply changes cleanly unless DB is wiped.
        await conn.run_sync(Base.metadata.create_all)
    await seed_db()
    yield

app = FastAPI(title="MediFlow AI V2", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(doctor.router, prefix="/api/doctors", tags=["Doctors"])
app.include_router(appointments.router, prefix="/api/appointments", tags=["Appointments"])

@app.get("/")
def health_check():
    return {"status": "ok", "message": "MediFlow AI V2 Backend is running."}
