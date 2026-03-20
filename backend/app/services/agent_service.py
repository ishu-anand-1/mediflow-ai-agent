import os
import json

from app.tools.availability import check_doctor_availability
from app.tools.booking import book_appointment
from app.tools.stats import get_appointments_stats
from app.tools.doctor_search import find_doctors_by_specialization
from app.tools.email import send_email

from app.utils.memory import get_memory, save_memory
from app.utils.logger import log_tool_call

# =========================
# 🤖 LLM SETUP (SARVAM)
# =========================
USE_LLM = False

try:
    from sarvamai import SarvamAI

    client = SarvamAI(
        api_subscription_key=os.getenv("SARVAM_API_KEY")
    )
    USE_LLM = True
    print("✅ LLM ENABLED (Sarvam)")
except:
    print("⚠️ LLM NOT AVAILABLE (Using fallback)")


# =========================
# 🧠 SAFE JSON PARSER
# =========================
def safe_json_parse(text):
    try:
        return json.loads(text)
    except:
        return {}


# =========================
# 🧠 RULE-BASED FALLBACK
# =========================
def map_symptom(text):
    text = text.lower()

    if "stomach" in text:
        return "Gastroenterologist"
    elif "fever" in text:
        return "General Physician"
    elif "skin" in text:
        return "Dermatologist"

    return "General Physician"


def detect_intent(text):
    text = text.lower()

    if "book" in text:
        return "book"
    elif "available" in text or "slot" in text:
        return "availability"
    elif "patients" in text or "report" in text:
        return "stats"

    return "availability"


# =========================
# 🤖 MAIN AGENT
# =========================
def run_agent(user_id, user_input, db):

    history = get_memory(user_id)
    save_memory(user_id, {"role": "user", "content": user_input})

    data = {}

    # =========================
    # 🧠 STEP 1: LLM UNDERSTANDING
    # =========================
    if USE_LLM:
        try:
            prompt = f"""
            Extract structured info from this:

            "{user_input}"

            Return ONLY JSON:
            {{
                "intent": "book | availability | stats",
                "symptom": "...",
                "doctor": "...",
                "date": "...",
                "time": "..."
            }}
            """

            response = client.chat.completions(
                model="sarvam-30b",
                messages=[
                    {"role": "system", "content": "You are a medical AI assistant."},
                    {"role": "user", "content": prompt}
                ]
            )

            raw_output = response["choices"][0]["message"]["content"]

            data = safe_json_parse(raw_output)

        except Exception as e:
            print("❌ LLM Error:", str(e))
            data = {}

    # =========================
    # 🔄 STEP 2: FALLBACK EXTRACTION
    # =========================
    intent = data.get("intent") or detect_intent(user_input)
    symptom = data.get("symptom") or user_input

    specialization = map_symptom(symptom)

    doctor = data.get("doctor") or "Dr Ahuja"
    date = data.get("date") or "tomorrow"
    time = data.get("time") or "10:30 AM"

    # =========================
    # 🔍 STEP 3: FIND DOCTORS
    # =========================
    log_tool_call("find_doctors", {"specialization": specialization})

    doctors = find_doctors_by_specialization(db, specialization)

    if not doctors:
        return {"message": f"No doctors found for {specialization}"}

    doctor = doctors[0]["name"]

    # =========================
    # 📅 STEP 4: CHECK AVAILABILITY
    # =========================
    log_tool_call("check_availability", {
        "doctor": doctor,
        "date": date
    })

    slots = check_doctor_availability(doctor, date)

    # =========================
    # 📅 STEP 5: BOOKING FLOW
    # =========================
    if intent == "book":

        if time not in slots:
            return {
                "message": f"{doctor} not available at {time}. Available slots: {', '.join(slots)}",
                "suggestion": slots
            }

        log_tool_call("book_appointment", {
            "patient": user_id,
            "doctor": doctor,
            "date": date,
            "time": time
        })

        booking = book_appointment(
            db=db,
            patient=user_id,
            doctor=doctor,
            date=date,
            time=time
        )

        # =========================
        # 📧 STEP 6: SEND EMAIL
        # =========================
        log_tool_call("send_email", {})

        send_email(
            email=f"{user_id}@mail.com",  # demo email
            message=f"Appointment confirmed with {doctor} at {time}"
        )

        return {
            "message": f"✅ Appointment booked with {doctor} at {time}",
            "doctor": doctor,
            "specialization": specialization,
            "status": "confirmed"
        }

    # =========================
    # 📊 STEP 7: STATS
    # =========================
    if intent == "stats":

        log_tool_call("get_stats", {})

        stats = get_appointments_stats(db, "today")

        return {
            "message": f"You handled {stats['total']} patients today"
        }

    # =========================
    # 🔍 ONLY AVAILABILITY
    # =========================
    return {
        "message": f"{doctor} is available at: {', '.join(slots)}",
        "doctor": doctor,
        "specialization": specialization
    }