from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine.url import make_url

from app.core.config import settings

# =========================
# 🗄️ DATABASE CONFIG
# =========================
DATABASE_URL = settings.DATABASE_URL

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL is missing in .env")

print("🚀 DATABASE CONNECTED:", DATABASE_URL)

# =========================
# 🔍 DETECT DB TYPE
# =========================
url = make_url(DATABASE_URL)
DB_TYPE = url.get_backend_name()

# =========================
# 🔥 ENGINE CONFIG
# =========================
if DB_TYPE == "sqlite":
    print("⚠️ Using SQLite (Development only)")

    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=True
    )

else:
    print("🐘 Using PostgreSQL (Production Ready)")

    engine = create_engine(
        DATABASE_URL,
        echo=True,              # 🔥 SQL logs
        pool_pre_ping=True,     # 🔥 auto reconnect
        pool_size=5,            # 🔥 connection pool
        max_overflow=10,
        future=True
    )

# =========================
# 🔄 SESSION FACTORY
# =========================
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

# =========================
# 🧱 BASE MODEL
# =========================
Base = declarative_base()

# =========================
# 🔗 DB DEPENDENCY (FastAPI)
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()   # 🔥 VERY IMPORTANT
        raise e
    finally:
        db.close()