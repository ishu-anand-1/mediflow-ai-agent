import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


def send_email(email: str, message: str):
    """
    📧 Send email (Mock + Optional SMTP support)
    """

    try:
        # =========================
        # 🔥 CONFIG (ENV BASED)
        # =========================
        SMTP_SERVER = os.getenv("SMTP_SERVER")
        SMTP_PORT = os.getenv("SMTP_PORT")
        SMTP_EMAIL = os.getenv("SMTP_EMAIL")
        SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

        # =========================
        # 🧪 MOCK MODE (NO SMTP)
        # =========================
        if not SMTP_SERVER:
            print("📧 MOCK EMAIL MODE")
            print(f"[EMAIL SENT] To: {email}")
            print(f"Message: {message}")

            return {
                "status": "success",
                "mode": "mock",
                "email": email,
                "message": message
            }

        # =========================
        # 📧 REAL EMAIL (SMTP)
        # =========================
        msg = MIMEMultipart()
        msg["From"] = SMTP_EMAIL
        msg["To"] = email
        msg["Subject"] = "Appointment Confirmation"

        msg.attach(MIMEText(message, "plain"))

        server = smtplib.SMTP(SMTP_SERVER, int(SMTP_PORT))
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)

        server.send_message(msg)
        server.quit()

        return {
            "status": "success",
            "mode": "smtp",
            "email": email
        }

    except Exception as e:
        print("❌ Email Error:", str(e))

        return {
            "status": "failed",
            "error": str(e)
        }