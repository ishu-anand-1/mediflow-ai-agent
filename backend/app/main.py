from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.database import Base, engine

# 🔥 IMPORT ROUTES
from app.api.routes import chat, doctor, appointment, user

# 🔥 IMPORT MODELS (REQUIRED for table creation)
import app.models.appointment
import app.models.user
import app.models.doctor


# =========================
# 🚀 STARTUP & SHUTDOWN
# =========================
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting MediFlow AI...")

    # 🔥 Create DB tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")

    yield

    print("🛑 Shutting down MediFlow AI...")


# =========================
# 🚀 CREATE APP
# =========================
app = FastAPI(
    title="MediFlow AI",
    version="1.0.0",
    description="AI-powered doctor recommendation and appointment booking system",
    lifespan=lifespan
)


# =========================
# 🌐 CORS CONFIG
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔥 Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# ❤️ HEALTH CHECK
# =========================
@app.get("/")
def root():
    return {
        "message": "🚀 MediFlow AI is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "MediFlow AI"
    }


# =========================
# 📡 REGISTER ROUTES (CLEAN PREFIX)
# =========================
app.include_router(chat.router, prefix="/api", tags=["AI Chat"])
app.include_router(doctor.router, prefix="/api", tags=["Doctor"])
app.include_router(appointment.router, prefix="/api", tags=["Appointments"])
app.include_router(user.router, prefix="/api", tags=["Users"])