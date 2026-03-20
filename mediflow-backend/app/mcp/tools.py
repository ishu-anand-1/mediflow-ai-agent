from typing import List, Optional
import json

MCP_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "find_doctors",
            "description": "Find recommended doctors internally mapped from given symptoms or explicit specialization.",
            "parameters": {
                "type": "object",
                "properties": {
                    "specialization": {
                        "type": "string",
                        "description": "The exact medical specialization (e.g., 'Gastroenterologist', 'Oncologist')"
                    },
                    "location": {
                        "type": "string",
                        "description": "City or specific location"
                    }
                },
                "required": ["specialization"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_availability",
            "description": "Check available time slots for a specific doctor.",
            "parameters": {
                "type": "object",
                "properties": {
                    "doctor_id": {
                        "type": "integer",
                        "description": "Doctor's ID"
                    },
                    "date": {
                        "type": "string",
                        "description": "Date in YYYY-MM-DD format"
                    },
                    "time_range": {
                        "type": "string",
                        "description": "E.g. 'morning', 'afternoon', 'any'"
                    }
                },
                "required": ["doctor_id", "date", "time_range"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "book_appointment",
            "description": "Book a doctor's appointment.",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_name": {
                        "type": "string",
                        "description": "Name of the patient booking the appointment"
                    },
                    "patient_email": {
                        "type": "string",
                        "description": "Email address of the patient for confirmations"
                    },
                    "doctor_id": {
                        "type": "integer",
                        "description": "Doctor's ID"
                    },
                    "date": {
                        "type": "string",
                        "description": "Date of appointment in YYYY-MM-DD format"
                    },
                    "time": {
                        "type": "string",
                        "description": "Exact time like '10:00'"
                    },
                    "disease": {
                        "type": "string",
                        "description": "The disease or symptoms reported"
                    }
                },
                "required": ["patient_name", "doctor_id", "date", "time", "disease"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "Send a confirmation email to the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "to_email": {
                        "type": "string",
                        "description": "Recipient email address"
                    },
                    "subject": {
                        "type": "string",
                        "description": "Email subject"
                    },
                    "message": {
                        "type": "string",
                        "description": "Email body content"
                    }
                },
                "required": ["to_email", "subject", "message"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_appointment_stats",
            "description": "Get total number of appointments for a given date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "Date to query in YYYY-MM-DD format"
                    }
                },
                "required": ["date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_disease_stats",
            "description": "Get count of patients recorded with a specific disease.",
            "parameters": {
                "type": "object",
                "properties": {
                    "disease": {
                        "type": "string",
                        "description": "Disease or symptom to query"
                    }
                },
                "required": ["disease"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_doctor_analytics",
            "description": "Fetch the daily appointment report dynamically for a specific doctor by name or ID (e.g. 'I am Dr Ahuja, how many patients today?'). Returns exact load distribution.",
            "parameters": {
                "type": "object",
                "properties": {
                    "doctor_name": {"type": "string", "description": "The name of the doctor (e.g., 'Dr Ahuja', 'Sarah')"},
                    "doctor_id": {"type": "integer", "description": "The ID of the doctor (optional)"}
                },
                "required": ["doctor_name"]
            }
        }
    }
]
