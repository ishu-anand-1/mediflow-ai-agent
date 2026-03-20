import uvicorn
import os
from app.core.config import settings


def main():
    try:
        # =========================
        # 🌐 SERVER CONFIG
        # =========================
        host = os.getenv("HOST", "127.0.0.1")
        port = int(os.getenv("PORT", 8000))
        reload = os.getenv("RELOAD", "true").lower() == "true"

        # =========================
        # 🔒 FORCE POSTGRESQL ONLY
        # =========================
        db_url = settings.DATABASE_URL

        if not db_url or not db_url.startswith("postgresql"):
            raise ValueError(
                f"❌ Invalid DATABASE_URL: {db_url}\n"
                "👉 Only PostgreSQL is allowed"
            )

        # =========================
        # 🚀 START LOGS
        # =========================
        print("\n========== SERVER START ==========")
        print("🚀 Starting MediFlow AI Server...")
        print(f"🌐 Host: {host}")
        print(f"📦 Port: {port}")
        print(f"🔄 Reload: {reload}")
        print(f"🐘 Database: PostgreSQL ✅")
        print("=================================\n")

        # =========================
        # 🚀 RUN UVICORN
        # =========================
        uvicorn.run(
            "app.main:app",
            host=host,
            port=port,
            reload=reload,
            workers=1 if reload else 4  # 🔥 dev vs prod
        )

    except Exception as e:
        print("\n❌ SERVER START FAILED")
        print(str(e))
        print("Fix your .env DATABASE_URL\n")


if __name__ == "__main__":
    main()