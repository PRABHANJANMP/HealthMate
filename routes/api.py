# routes/api.py
"""
General API & System Health Check Routes
"""

from fastapi import APIRouter

router = APIRouter(tags=["System"])

@router.get("/health")
def health_check():
    return {
        "status": "online",
        "assistant": "HealthMate AI - Bilingual Health Assistant",
        "ai_model": "gemini-2.0-flash",
        "sdk": "strands-agents",
        "backend": "Python FastAPI + Jinja2"
    }
