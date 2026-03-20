import os
from dotenv import load_dotenv
from pathlib import Path


# =========================
# 🔥 LOAD .env (ROBUST)
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"

print("📂 Looking for .env at:", ENV_PATH)

if not ENV_PATH.exists():
    raise FileNotFoundError(f"❌ .env file not found at {ENV_PATH}")

load_dotenv(dotenv_path=ENV_PATH)


class Settings:
    def __init__(self):
        # =========================
        # 🗄️ DATABASE
        # =========================
        self.DATABASE_URL: str | None = os.getenv("DATABASE_URL")

        # =========================
        # 🤖 AI KEYS
        # =========================
        self.SARVAM_API_KEY: str = os.getenv("SARVAM_API_KEY", "")

        # =========================
        # ⚙️ APP SETTINGS
        # =========================
        self.DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

        # =========================
        # 🔍 DEBUG RAW ENV
        # =========================
        print("🔍 RAW DATABASE_URL:", self.DATABASE_URL)

        # =========================
        # 🚨 VALIDATION
        # =========================
        if not self.DATABASE_URL:
            raise ValueError("❌ DATABASE_URL is missing in .env file")

        if not self.DATABASE_URL.startswith("postgresql"):
            raise ValueError(
                f"❌ Invalid DB: {self.DATABASE_URL}\n"
                "👉 Only PostgreSQL is allowed"
            )

        # =========================
        # ✅ SUCCESS LOG
        # =========================
        print("\n========== CONFIG ==========")
        print("✅ CONFIG LOADED SUCCESSFULLY")
        print("🐘 DATABASE:", self.DATABASE_URL)
        print("🤖 SARVAM:", "Loaded ✅" if self.SARVAM_API_KEY else "Not Found ⚠️")
        print("============================\n")


# =========================
# 🔥 SINGLETON INSTANCE
# =========================
settings = Settings()