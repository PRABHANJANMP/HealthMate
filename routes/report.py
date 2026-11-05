# routes/report.py
"""
Monthly Doctor Report Compilation & Tele-Sharing Routes
"""

import urllib.parse
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from services.vitals_service import get_patient_logs, compute_vitals_statistics
from services.agent_service import summarize_doctor_report

router = APIRouter(tags=["Doctor Report"])

class DoctorReportRequest(BaseModel):
    patient_id: str = Field(default="default")
    patient_name: Optional[str] = "Patient"
    age: Optional[str] = None
    language: str = Field(default="English")
    doctor_email: Optional[str] = None
    doctor_phone: Optional[str] = None

def build_report_data(patient_name: str, patient_age: str, doctor_email: str, doctor_phone: str, lang: str):
    is_ta = lang == "Tamil"
    patient_logs = get_patient_logs("default")

    stats = compute_vitals_statistics(patient_logs)

    vitals_text = (
        f"Patient: {patient_name} (Age/Gender: {patient_age or 'Unspecified'})\n"
        f"Total Daily Entries: {stats['total_days_logged']}\n"
        f"BP Averages: {stats['avg_systolic_bp']}/{stats['avg_diastolic_bp']} mmHg (Peak: {stats['max_bp']})\n"
        f"Blood Sugar: Avg {stats['avg_blood_glucose']} mg/dL (Peak: {stats['max_glucose']} mg/dL)\n"
        f"Oxygen SpO2: Avg {stats['avg_spo2']}% (Lowest: {stats['min_spo2']}%)\n"
        f"Heart Rate: Avg {stats['avg_pulse']} BPM\n"
        f"Temperature: Avg {stats['avg_temp']}°F (Peak: {stats['max_temp']}°F)\n"
        f"Symptom Summary: {stats['symptom_frequencies']}\n"
        f"Red Flags Detected: {', '.join(stats['red_flags']) if stats['red_flags'] else 'None recorded'}"
    )

    clinical_summary = summarize_doctor_report(vitals_text, lang)
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Build mailto URL
    email_subject = urllib.parse.quote(
        f"மாதாந்திர மருத்துவ அறிக்கை: {patient_name} ({generated_at})" if is_ta
        else f"Monthly Vitals Clinical Handover: {patient_name} ({generated_at})"
    )
    email_body = urllib.parse.quote(
        (f"வணக்கம் மருத்துவர் அவர்களுக்கு,\n\nநோயாளி {patient_name} ({patient_age}) அவர்களின் மாதாந்திர உடல்நல அளவீட்டு அறிக்கை கீழே இணைக்கப்பட்டுள்ளது.\n\n"
         if is_ta else
         f"Dear Doctor,\n\nPlease find the monthly home vitals report for patient: {patient_name} ({patient_age}).\n\n") +
        (f"உடல்நல அளவீடுகள் சுருக்கம் (கடந்த 30 நாட்கள்):\n" if is_ta else "VITALS OVERVIEW (Past 30 Days):\n") +
        f"- Average BP: {stats['avg_systolic_bp']}/{stats['avg_diastolic_bp']} mmHg (Peak: {stats['max_bp']})\n" +
        f"- Blood Sugar: Avg {stats['avg_blood_glucose']} mg/dL (Peak: {stats['max_glucose']})\n" +
        f"- Oxygen SpO2: Avg {stats['avg_spo2']}% (Lowest: {stats['min_spo2']}%)\n" +
        f"- Heart Rate: Avg {stats['avg_pulse']} BPM\n" +
        f"- Temperature: Avg {stats['avg_temp']}°F\n\n" +
        (f"மருத்துவ குறிப்புரை:\n{clinical_summary}\n\nHealthMate AI." if is_ta
         else f"CLINICAL SUMMARY NOTE:\n{clinical_summary}\n\nHealthMate AI.")
    )
    email_link = f"mailto:{doctor_email or ''}?subject={email_subject}&body={email_body}"

    # Build WhatsApp URL
    clean_phone = "".join(c for c in (doctor_phone or "") if c.isdigit())
    phone_param = f"phone={clean_phone}&" if clean_phone else ""
    wa_text = urllib.parse.quote(
        (f"*🏥 HealthMate AI - மாதாந்திர உடல்நல அறிக்கை*\n*நோயாளி:* {patient_name} ({patient_age})\n\n"
         f"*BP:* {stats['avg_systolic_bp']}/{stats['avg_diastolic_bp']} mmHg\n"
         f"*சர்க்கரை:* {stats['avg_blood_glucose']} mg/dL\n*SpO2:* {stats['avg_spo2']}%\n\n"
         f"*மருத்துவ குறிப்பு:* {clinical_summary}"
         if is_ta else
         f"*🏥 HealthMate AI - Monthly Patient Vitals Summary*\n*Patient:* {patient_name} ({patient_age})\n\n"
         f"*BP:* {stats['avg_systolic_bp']}/{stats['avg_diastolic_bp']} mmHg\n"
         f"*Sugar:* Avg {stats['avg_blood_glucose']} mg/dL\n*SpO2:* {stats['avg_spo2']}%\n\n"
         f"*Clinical Note:* {clinical_summary}")
    )
    whatsapp_link = f"https://api.whatsapp.com/send?{phone_param}text={wa_text}"

    return {
        "patient_name": patient_name,
        "patient_age": patient_age,
        "doctor_email": doctor_email,
        "doctor_phone": doctor_phone,
        "generated_at": generated_at,
        "stats": stats,
        "clinical_summary": clinical_summary,
        "red_flags": stats["red_flags"],
        "email_link": email_link,
        "whatsapp_link": whatsapp_link,
    }

@router.post("/doctor-report/generate")
async def generate_report_form(
    request: Request,
    patient_name: str = Form(default="Ramesh Kumar"),
    patient_age: str = Form(default="48 Y / Male"),
    doctor_email: Optional[str] = Form(default=""),
    doctor_phone: Optional[str] = Form(default=""),
    language: Optional[str] = Form(default="English"),
):
    lang = "Tamil" if language in ("Tamil", "ta") else "English"
    report = build_report_data(patient_name, patient_age, doctor_email or "", doctor_phone or "", lang)
    
    # Store report in request state / redirect with parameters
    return RedirectResponse(
        url=f"/?tab=report&lang={lang}&report_ready=1&p_name={urllib.parse.quote(patient_name)}&p_age={urllib.parse.quote(patient_age)}&d_email={urllib.parse.quote(doctor_email or '')}&d_phone={urllib.parse.quote(doctor_phone or '')}",
        status_code=303
    )

@router.post("/api/doctor-report")
def api_doctor_report(req: DoctorReportRequest):
    lang = "Tamil" if req.language in ("Tamil", "ta") else "English"
    report = build_report_data(
        req.patient_name or "Patient",
        req.age or "Unspecified",
        req.doctor_email or "",
        req.doctor_phone or "",
        lang
    )
    return {"success": True, "report": report}
