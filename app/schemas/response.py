from typing import Any, Optional


def success_response(data: Any, message: Optional[str] = None):
    return {
        "success": True,
        "message": message,
        "data": data
    }


def error_response(message: str):
    return {
        "success": False,
        "message": message,
        "data": None
    }