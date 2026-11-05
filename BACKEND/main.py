"""
Bilingual AI Health Assistant - FastAPI Backend
Run with: uvicorn main:app --reload
"""

import json
import os
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from agent import run_health_agent, get_session_history, clear_session, summarize_doctor_report



# ---------------------------------------------------------------------------
# FastAPI app setup
# ---------------------------------------------------------------------------

app = FastAPI(
    title="HealthMate AI - Bilingual Health Assistant",
    description=(
        "An AI-powered health assistant supporting Tamil and English. "
        "Built with Strands Agents SDK and Google Gemini 2.0 Flash."
    ),
    version="2.0.0",
)


# ---------------------------------------------------------------------------
# CORS - allow all origins for local/hackathon use
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Request and response models
# ---------------------------------------------------------------------------

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000,
                         description="The user health question")
    language: str = Field(default="English",
                          description="Response language: English or Tamil")
    session_id: str = Field(default="default",
                            description="Unique session ID for conversation memory")


class ChatResponse(BaseModel):
    success: bool
    language: str
    reply: str
    is_emergency: bool
    session_id: str


class HistoryResponse(BaseModel):
    session_id: str
    message_count: int
    messages: list


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/")
def home():
    """API home - confirms the server is running."""
    return {
        "message": "HealthMate AI is running!",
        "version": "2.0.0",
        "languages": ["English", "Tamil"],
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    """Backend health check endpoint."""
    return {
        "status": "online",
        "assistant": "HealthMate AI - Bilingual Health Assistant",
        "ai_model": "gemini-2.0-flash",
        "sdk": "strands-agents",
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Main chat endpoint. Accepts a health question and returns an AI response.
    Automatically detects emergencies and flags them.
    """

    # Validate message content
    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Please enter a health question."
        )

    # Validate language
    if request.language not in ("English", "Tamil"):
        raise HTTPException(
            status_code=400,
            detail="Language must be either 'English' or 'Tamil'."
        )

    # Run the health agent
    try:
        reply_text, is_emergency = run_health_agent(
            message=request.message.strip(),
            language=request.language,
            session_id=request.session_id,
        )

        return ChatResponse(
            success=True,
            language=request.language,
            reply=reply_text,
            is_emergency=is_emergency,
            session_id=request.session_id,
        )

    except Exception as error:
        # Log the error for debugging
        print(f"[ERROR] /chat endpoint - session={request.session_id}: {error}")

        # Return a user-friendly error message in the requested language
        if request.language == "Tamil":
            error_message = (
                "மன்னிக்கவும். தற்போது AI சேவையை அணுக முடியவில்லை. "
                "சிறிது நேரம் கழித்து மீண்டும் முயற்சிக்கவும். "
                "அவசர நிலையில் 108 அழையுங்கள்."
            )
        else:
            error_message = (
                "Sorry, the AI service is temporarily unavailable. "
                "Please try again in a moment. "
                "In an emergency, call 108 immediately."
            )

        raise HTTPException(
            status_code=503,
            detail=error_message,
        )


@app.get("/history/{session_id}", response_model=HistoryResponse)
def get_history(session_id: str):
    """
    Retrieve the conversation history for a session.
    Returns a simplified list of messages.
    """
    messages = get_session_history(session_id)

    # Extract simplified message list (role + text only)
    simplified = []
    for msg in messages:
        role = msg.get("role", "unknown")
        content = msg.get("content", [])
        text = ""
        for block in content:
            if isinstance(block, dict) and "text" in block:
                text += block["text"]
        if text:
            simplified.append({"role": role, "text": text})

    return HistoryResponse(
        session_id=session_id,
        message_count=len(simplified),
        messages=simplified,
    )


@app.delete("/clear/{session_id}")
def clear_chat_history(session_id: str):
    """
    Clear the conversation history for a session.
    Call this when the user clicks the Clear Chat button.
    """
    clear_session(session_id)
    return {
        "success": True,
        "session_id": session_id,
        "message": "Conversation history cleared.",
    }


# ---------------------------------------------------------------------------
# Daily Health Log Models & Data Persistence
# ---------------------------------------------------------------------------

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
LOGS_FILE = os.path.join(DATA_DIR, "health_logs.json")
os.makedirs(DATA_DIR, exist_ok=True)


class DailyHealthLog(BaseModel):
    id: Optional[str] = None
    patient_id: str = Field(default="default", description="Identifier for patient or household member")
    date: str = Field(..., description="Date of entry YYYY-MM-DD")
    time: Optional[str] = None
    systolic_bp: Optional[int] = Field(default=None, description="Systolic Blood Pressure (mmHg)")
    diastolic_bp: Optional[int] = Field(default=None, description="Diastolic Blood Pressure (mmHg)")
    blood_glucose: Optional[int] = Field(default=None, description="Blood Sugar / Glucose (mg/dL)")
    heart_rate: Optional[int] = Field(default=None, description="Heart / Pulse Rate (BPM)")
    spo2: Optional[int] = Field(default=None, description="Blood Oxygen Saturation (%)")
    temperature: Optional[float] = Field(default=None, description="Body Temperature (°F)")
    pain_level: Optional[int] = Field(default=0, ge=0, le=10, description="Pain rating 0-10")
    symptoms: List[str] = Field(default_factory=list, description="Observed symptoms")
    condition_severity: str = Field(default="Mild", description="Mild, Moderate, or Severe")
    notes: Optional[str] = Field(default="", description="Patient observations, diet, medications taken")


class DoctorReportRequest(BaseModel):
    patient_id: str = Field(default="default")
    patient_name: Optional[str] = "Patient"
    age: Optional[int] = None
    gender: Optional[str] = None
    language: str = Field(default="English", description="English or Tamil")
    doctor_email: Optional[str] = None


def _load_all_logs() -> List[dict]:
    if not os.path.exists(LOGS_FILE):
        return []
    try:
        with open(LOGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_all_logs(logs: List[dict]):
    with open(LOGS_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)


@app.get("/api/health-logs")
def get_health_logs(patient_id: str = Query(default="default")):
    """Retrieve daily health logs for a patient."""
    all_logs = _load_all_logs()
    if patient_id != "all":
        logs = [entry for entry in all_logs if entry.get("patient_id", "default") == patient_id]
    else:
        logs = all_logs
    # Sort newest first
    logs.sort(key=lambda x: (x.get("date", ""), x.get("time", "")), reverse=True)
    return {"success": True, "count": len(logs), "logs": logs}


@app.post("/api/health-logs")
def save_health_log(entry: DailyHealthLog):
    """Save or update a daily health log entry."""
    all_logs = _load_all_logs()
    log_dict = entry.model_dump()
    if not log_dict.get("id"):
        log_dict["id"] = f"log_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    if not log_dict.get("time"):
        log_dict["time"] = datetime.now().strftime("%H:%M")

    # Replace existing or append
    existing_idx = next((i for i, item in enumerate(all_logs) if item.get("id") == log_dict["id"]), -1)
    if existing_idx >= 0:
        all_logs[existing_idx] = log_dict
    else:
        all_logs.append(log_dict)

    _save_all_logs(all_logs)
    return {"success": True, "message": "Health log entry saved successfully.", "entry": log_dict}


@app.delete("/api/health-logs/{patient_id}")
def delete_patient_logs(patient_id: str):
    """Clear health logs for a patient."""
    all_logs = _load_all_logs()
    remaining = [entry for entry in all_logs if entry.get("patient_id", "default") != patient_id]
    _save_all_logs(remaining)
    return {"success": True, "message": f"Logs cleared for patient {patient_id}."}


@app.post("/api/doctor-report")
def generate_monthly_doctor_report(req: DoctorReportRequest):
    """
    Compile past monthly health records into a structured clinical report
    with vital statistics, red flags, and an AI physician summary.
    """
    all_logs = _load_all_logs()
    patient_logs = [e for e in all_logs if e.get("patient_id", "default") == req.patient_id]

    if not patient_logs:
        raise HTTPException(status_code=404, detail="No health logs recorded yet for this patient.")

    # Calculate statistics
    bps_sys = [e["systolic_bp"] for e in patient_logs if e.get("systolic_bp")]
    bps_dia = [e["diastolic_bp"] for e in patient_logs if e.get("diastolic_bp")]
    glucoses = [e["blood_glucose"] for e in patient_logs if e.get("blood_glucose")]
    spo2s = [e["spo2"] for e in patient_logs if e.get("spo2")]
    temps = [e["temperature"] for e in patient_logs if e.get("temperature")]
    pulses = [e["heart_rate"] for e in patient_logs if e.get("heart_rate")]

    symptom_counts = {}
    for e in patient_logs:
        for s in e.get("symptoms", []):
            symptom_counts[s] = symptom_counts.get(s, 0) + 1

    red_flags = []
    if bps_sys and max(bps_sys) >= 140:
        red_flags.append(f"Elevated Systolic Blood Pressure detected (Peak: {max(bps_sys)} mmHg)")
    if bps_dia and max(bps_dia) >= 90:
        red_flags.append(f"Elevated Diastolic Blood Pressure detected (Peak: {max(bps_dia)} mmHg)")
    if glucoses and max(glucoses) >= 180:
        red_flags.append(f"High Blood Sugar reading logged (Peak: {max(glucoses)} mg/dL)")
    if spo2s and min(spo2s) < 95:
        red_flags.append(f"Hypoxia alert: Oxygen Saturation dipped to {min(spo2s)}%")
    if temps and max(temps) >= 101.0:
        red_flags.append(f"High Fever recorded (Peak: {max(temps)}°F)")

    stats = {
        "total_days_logged": len(patient_logs),
        "avg_systolic_bp": round(sum(bps_sys) / len(bps_sys)) if bps_sys else None,
        "avg_diastolic_bp": round(sum(bps_dia) / len(bps_dia)) if bps_dia else None,
        "max_bp": f"{max(bps_sys)}/{max(bps_dia)}" if bps_sys and bps_dia else None,
        "avg_blood_glucose": round(sum(glucoses) / len(glucoses)) if glucoses else None,
        "max_glucose": max(glucoses) if glucoses else None,
        "avg_pulse": round(sum(pulses) / len(pulses)) if pulses else None,
        "avg_spo2": round(sum(spo2s) / len(spo2s), 1) if spo2s else None,
        "min_spo2": min(spo2s) if spo2s else None,
        "avg_temp": round(sum(temps) / len(temps), 1) if temps else None,
        "max_temp": max(temps) if temps else None,
        "symptom_frequencies": symptom_counts,
        "red_flags": red_flags,
    }

    # Format text prompt for Gemini Agent
    vitals_text = (
        f"Patient: {req.patient_name} (Age: {req.age or 'Unspecified'}, Gender: {req.gender or 'Unspecified'})\n"
        f"Total Daily Entries: {stats['total_days_logged']}\n"
        f"BP Averages: {stats['avg_systolic_bp']}/{stats['avg_diastolic_bp']} mmHg (Peak: {stats['max_bp']})\n"
        f"Blood Sugar: Avg {stats['avg_blood_glucose']} mg/dL (Peak: {stats['max_glucose']} mg/dL)\n"
        f"Oxygen SpO2: Avg {stats['avg_spo2']}% (Lowest: {stats['min_spo2']}%)\n"
        f"Heart Rate: Avg {stats['avg_pulse']} BPM\n"
        f"Temperature: Avg {stats['avg_temp']}°F (Peak: {stats['max_temp']}°F)\n"
        f"Symptom Summary: {symptom_counts}\n"
        f"Red Flags Detected: {', '.join(red_flags) if red_flags else 'None recorded'}"
    )

    clinical_summary = summarize_doctor_report(vitals_text, req.language)

    return {
        "success": True,
        "patient_id": req.patient_id,
        "patient_name": req.patient_name,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "language": req.language,
        "doctor_email": req.doctor_email,
        "summary_stats": stats,
        "clinical_summary": clinical_summary,
        "red_flags": red_flags,
        "recent_logs": patient_logs[:15],
    }

