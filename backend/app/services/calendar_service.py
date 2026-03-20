from datetime import datetime, timedelta


def parse_date(date_str: str):
    """
    🔥 Converts natural text → actual date
    """
    today = datetime.now().date()

    if date_str.lower() == "today":
        return today

    if date_str.lower() == "tomorrow":
        return today + timedelta(days=1)

    # Try parsing custom date (YYYY-MM-DD)
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except:
        return today  # fallback


def create_calendar_event(doctor: str, date: str, time: str):
    try:
        # 🔥 Step 1: Parse date safely
        event_date = parse_date(date)

        # 🔥 Step 2: Convert time (basic handling)
        try:
            event_time = datetime.strptime(time, "%I:%M %p").time()
        except:
            event_time = datetime.now().time()

        # 🔥 Step 3: Combine into datetime
        scheduled_at = datetime.combine(event_date, event_time)

        # 🔥 MOCK RESPONSE (replace with Google Calendar later)
        return {
            "status": "success",
            "message": "📅 Calendar event created",
            "data": {
                "doctor": doctor,
                "scheduled_at": scheduled_at.isoformat()
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "message": "Failed to create calendar event",
            "error": str(e)
        }