# routes/vitals.py
"""
Daily Health Logs & Vitals Tracking Routes
"""

from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Form, Request, Query
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from services.vitals_service import (
    load_all_logs,
    save_health_log,
    get_patient_logs,
    delete_health_log,
)

router = APIRouter(tags=["Vitals"])

class DailyHealthLogModel(BaseModel):
    id: Optional[str] = None
    patient_id: str = Field(default="default")
    date: str
    time: Optional[str] = None
    systolic_bp: Optional[int] = None
    diastolic_bp: Optional[int] = None
    blood_glucose: Optional[int] = None
    heart_rate: Optional[int] = None
    spo2: Optional[int] = None
    temperature: Optional[float] = None
    pain_level: Optional[int] = 0
    symptoms: List[str] = Field(default_factory=list)
    condition_severity: str = "Mild"
    notes: Optional[str] = ""

@router.post("/daily-log")
async def submit_daily_log_form(
    request: Request,
    date: str = Form(...),
    time: str = Form(default=""),
    systolic_bp: Optional[str] = Form(default=None),
    diastolic_bp: Optional[str] = Form(default=None),
    blood_glucose: Optional[str] = Form(default=None),
    heart_rate: Optional[str] = Form(default=None),
    spo2: Optional[str] = Form(default=None),
    temperature: Optional[str] = Form(default=None),
    pain_level: Optional[str] = Form(default="0"),
    condition_severity: str = Form(default="Mild"),
    notes: Optional[str] = Form(default=""),
):
    form_data = await request.form()
    symptoms_list = form_data.getlist("symptoms")

    def to_int(val):
        try:
            return int(val) if val and str(val).strip() else None
        except (ValueError, TypeError):
            return None

    def to_float(val):
        try:
            return float(val) if val and str(val).strip() else None
        except (ValueError, TypeError):
            return None

    entry = {
        "id": f"log_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
        "patient_id": "default",
        "date": date,
        "time": time or datetime.now().strftime("%H:%M"),
        "systolic_bp": to_int(systolic_bp),
        "diastolic_bp": to_int(diastolic_bp),
        "blood_glucose": to_int(blood_glucose),
        "heart_rate": to_int(heart_rate),
        "spo2": to_int(spo2),
        "temperature": to_float(temperature),
        "pain_level": to_int(pain_level) or 0,
        "symptoms": list(symptoms_list),
        "condition_severity": condition_severity,
        "notes": (notes or "").strip(),
    }

    save_health_log(entry)

    lang = request.cookies.get("healthmate_lang", "English")
    return RedirectResponse(url=f"/?tab=chart&lang={lang}&saved=1", status_code=303)

@router.post("/daily-log/delete/{log_id}")
def delete_daily_log_form(request: Request, log_id: str):
    delete_health_log(log_id)
    lang = request.cookies.get("healthmate_lang", "English")
    return RedirectResponse(url=f"/?tab=chart&lang={lang}", status_code=303)

@router.get("/api/health-logs")
def api_get_health_logs(patient_id: str = Query(default="default")):
    logs = get_patient_logs(patient_id)
    return {"success": True, "count": len(logs), "logs": logs}

@router.post("/api/health-logs")
def api_save_health_log(entry: DailyHealthLogModel):
    saved = save_health_log(entry.model_dump())
    return {"success": True, "message": "Saved.", "entry": saved}
