# services/vitals_service.py
"""
Daily Health Logs & Clinical Vitals Analysis Service
Manages JSON storage, demo data seeding, and statistical calculation.
"""

import os
import json
from datetime import datetime
from typing import Optional, List, Dict, Any

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
LOGS_FILE = os.path.join(DATA_DIR, "health_logs.json")
os.makedirs(DATA_DIR, exist_ok=True)

DEMO_SEEDS = [
    {
        "id": "seed_1",
        "patient_id": "default",
        "date": "2026-10-10",
        "time": "08:30",
        "systolic_bp": 138,
        "diastolic_bp": 88,
        "blood_glucose": 142,
        "heart_rate": 76,
        "spo2": 97,
        "temperature": 98.6,
        "pain_level": 2,
        "symptoms": ["Headache"],
        "condition_severity": "Mild",
        "notes": "Morning measurement after waking up."
    },
    {
        "id": "seed_2",
        "patient_id": "default",
        "date": "2026-10-18",
        "time": "19:00",
        "systolic_bp": 144,
        "diastolic_bp": 92,
        "blood_glucose": 168,
        "heart_rate": 84,
        "spo2": 96,
        "temperature": 99.8,
        "pain_level": 4,
        "symptoms": ["Fever", "Body Ache"],
        "condition_severity": "Moderate",
        "notes": "Felt warm and fatigued. Took Paracetamol 650mg."
    },
    {
        "id": "seed_3",
        "patient_id": "default",
        "date": "2026-10-25",
        "time": "08:15",
        "systolic_bp": 130,
        "diastolic_bp": 84,
        "blood_glucose": 125,
        "heart_rate": 72,
        "spo2": 98,
        "temperature": 98.4,
        "pain_level": 1,
        "symptoms": [],
        "condition_severity": "Mild",
        "notes": "Good rest, vitals normal."
    },
    {
        "id": "seed_4",
        "patient_id": "default",
        "date": "2026-11-02",
        "time": "14:40",
        "systolic_bp": 148,
        "diastolic_bp": 94,
        "blood_glucose": 185,
        "heart_rate": 88,
        "spo2": 95,
        "temperature": 100.5,
        "pain_level": 5,
        "symptoms": ["Fever", "Headache", "Cough"],
        "condition_severity": "Moderate",
        "notes": "High glucose after festival food. Wet cloth compress applied."
    }
]

def load_all_logs() -> List[Dict[str, Any]]:
    if not os.path.exists(LOGS_FILE):
        save_all_logs(DEMO_SEEDS)
        return list(DEMO_SEEDS)
    try:
        with open(LOGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not data:
                save_all_logs(DEMO_SEEDS)
                return list(DEMO_SEEDS)
            return data
    except Exception:
        save_all_logs(DEMO_SEEDS)
        return list(DEMO_SEEDS)

def save_all_logs(logs: List[Dict[str, Any]]) -> None:
    with open(LOGS_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)

def get_patient_logs(patient_id: str = "default") -> List[Dict[str, Any]]:
    all_logs = load_all_logs()
    if patient_id != "all":
        logs = [e for e in all_logs if e.get("patient_id", "default") == patient_id]
    else:
        logs = all_logs
    logs.sort(key=lambda x: (x.get("date", ""), x.get("time", "")), reverse=True)
    return logs

def save_health_log(entry: Dict[str, Any]) -> Dict[str, Any]:
    all_logs = load_all_logs()
    if not entry.get("id"):
        entry["id"] = f"log_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    if not entry.get("time"):
        entry["time"] = datetime.now().strftime("%H:%M")
    if not entry.get("patient_id"):
        entry["patient_id"] = "default"

    idx = next((i for i, item in enumerate(all_logs) if item.get("id") == entry["id"]), -1)
    if idx >= 0:
        all_logs[idx] = entry
    else:
        all_logs.append(entry)

    save_all_logs(all_logs)
    return entry

def delete_health_log(log_id: str) -> bool:
    all_logs = load_all_logs()
    initial_len = len(all_logs)
    all_logs = [e for e in all_logs if e.get("id") != log_id]
    if len(all_logs) < initial_len:
        save_all_logs(all_logs)
        return True
    return False

def compute_vitals_statistics(patient_logs: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not patient_logs:
        return {
            "total_days_logged": 0,
            "avg_systolic_bp": None,
            "avg_diastolic_bp": None,
            "max_bp": None,
            "avg_blood_glucose": None,
            "max_glucose": None,
            "avg_pulse": None,
            "avg_spo2": None,
            "min_spo2": None,
            "avg_temp": None,
            "max_temp": None,
            "symptom_frequencies": {},
            "red_flags": [],
        }

    bps_sys = [e["systolic_bp"] for e in patient_logs if e.get("systolic_bp")]
    bps_dia = [e["diastolic_bp"] for e in patient_logs if e.get("diastolic_bp")]
    glucoses = [e["blood_glucose"] for e in patient_logs if e.get("blood_glucose")]
    spo2s = [e["spo2"] for e in patient_logs if e.get("spo2")]
    temps = [e["temperature"] for e in patient_logs if e.get("temperature")]
    pulses = [e["heart_rate"] for e in patient_logs if e.get("heart_rate")]

    symptom_counts: Dict[str, int] = {}
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

    return {
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
