import json
from datetime import datetime


def log_tool_call(name: str, args: dict):
    """
    🔧 Logs tool execution in structured format
    """

    log = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": "INFO",
        "tool_called": name,
        "input": args
    }

    print(json.dumps(log, indent=2))


def log_error(message: str, error: str = ""):
    """
    ❌ Logs errors
    """

    log = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": "ERROR",
        "message": message,
        "error": error
    }

    print(json.dumps(log, indent=2))