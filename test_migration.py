# test_migration.py
"""
Comprehensive Verification Suite for Bilingual AI Health Assistant Migration
Tests all pages, routes, bilingual functionality, AI agent, and offline guides.
"""

import sys
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_routes():
    print("--- 1. Testing GET / (English Home) ---")
    resp = client.get("/")
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    assert "HealthMate AI" in resp.text
    assert "Chat" in resp.text
    assert "Offline First-Aid" in resp.text
    print("✓ GET / (English) passed!")

    print("--- 2. Testing GET /?lang=Tamil (Tamil Home) ---")
    resp = client.get("/?lang=Tamil")
    assert resp.status_code == 200
    assert "அரட்டை" in resp.text
    assert "அவசர முதலுதவி" in resp.text
    print("✓ GET /?lang=Tamil passed!")

    print("--- 3. Testing GET /first-aid (First-Aid Guide) ---")
    resp = client.get("/?tab=wounds&wound=snakebites&lang=Tamil")
    assert resp.status_code == 200
    assert "பாம்பு கடி" in resp.text
    assert "Anti-Snake Venom" in resp.text or "ASV" in resp.text
    print("✓ First-Aid Tamil Snakebite Protocol passed!")

    print("--- 4. Testing GET /medicine-kit (Medicine Checklist) ---")
    resp = client.get("/?tab=meds&category=fever&lang=English")
    assert resp.status_code == 200
    assert "Paracetamol" in resp.text
    print("✓ Medicine Kit filtering passed!")

    print("--- 5. Testing GET /daily-log (Daily Log & Vitals) ---")
    resp = client.get("/?tab=chart&lang=English")
    assert resp.status_code == 200
    assert "Daily Health Check-in Entry" in resp.text
    assert "vitalsChart" in resp.text
    print("✓ Daily Log View & Charts passed!")

    print("--- 6. Testing GET /health (Health Check) ---")
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "online"
    assert data["ai_model"] == "gemini-2.0-flash"
    print("✓ /health API passed!", data)

    print("--- 7. Testing POST /daily-log (Form Submission) ---")
    form_data = {
        "date": "2026-11-05",
        "time": "10:30",
        "systolic_bp": "122",
        "diastolic_bp": "82",
        "blood_glucose": "110",
        "heart_rate": "74",
        "spo2": "99",
        "temperature": "98.6",
        "pain_level": "1",
        "condition_severity": "Mild",
        "notes": "Test vital measurement",
        "symptoms": ["Headache"]
    }
    resp = client.post("/daily-log", data=form_data, follow_redirects=False)
    assert resp.status_code in (302, 303), f"Expected redirect, got {resp.status_code}"
    print("✓ POST /daily-log saved and redirected successfully!")

    print("--- 8. Testing POST /chat (AI & Instant Clinical Engine) ---")
    chat_payload = {
        "message": "I have severe headache and mild fever, what first aid should I take?",
        "language": "English",
        "session_id": "test_suite_session"
    }
    resp = client.post("/chat", json=chat_payload)
    assert resp.status_code == 200
    res_data = resp.json()
    assert res_data["success"] is True
    assert len(res_data["reply"]) > 20
    print("✓ POST /chat English response received:", res_data["reply"][:100], "...")

    print("--- 9. Testing Emergency Detection in /chat ---")
    emergency_payload = {
        "message": "Chest pain radiating to left arm and heavy sweating",
        "language": "English",
        "session_id": "test_emergency_session"
    }
    resp = client.post("/chat", json=emergency_payload)
    assert resp.status_code == 200
    em_data = resp.json()
    assert em_data["is_emergency"] is True
    assert "108" in em_data["reply"]
    print("✓ Emergency 108 Alerting triggered correctly!")

    print("--- 10. Testing POST /doctor-report/generate ---")
    rep_form = {
        "patient_name": "Muthu Kumar",
        "patient_age": "52 Y / Male",
        "doctor_email": "doctor@testphc.org",
        "doctor_phone": "919876543210",
        "language": "English"
    }
    resp = client.post("/doctor-report/generate", data=rep_form, follow_redirects=False)
    assert resp.status_code in (302, 303)
    assert "report_ready=1" in resp.headers["location"]
    print("✓ Doctor Report generation redirected with report_ready!")

    print("--- 11. Testing Doctor Report Content Rendering ---")
    resp = client.get("/?tab=report&report_ready=1&p_name=Muthu+Kumar&p_age=52+Y+/+Male&lang=English")
    assert resp.status_code == 200
    assert "Muthu Kumar" in resp.text
    assert "Monthly Tele-Health Vitals Summary" in resp.text
    assert "mailto:" in resp.text
    assert "whatsapp.com" in resp.text
    print("✓ Doctor Report HTML view & sharing links verified!")

    print("--- 12. Testing Offline Standalone First-Aid Page ---")
    import os
    offline_file = os.path.join("static", "offline.html")
    assert os.path.exists(offline_file), "static/offline.html must exist for offline PWA!"
    with open(offline_file, "r", encoding="utf-8") as f:
        html = f.read()
    assert "Offline First-Aid Emergency" in html or "HealthMate AI" in html
    assert "108" in html
    print("✓ Standalone Offline First-Aid file verified!")

    print("\n🎉 ALL 12 TEST SUITES PASSED FLAWLESSLY!")

if __name__ == "__main__":
    test_routes()
