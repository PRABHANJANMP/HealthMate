# 🏥 HealthMate AI — Python Full-Stack Bilingual Health Assistant (தமிழ் / English)

> **AWS User Group Madurai Strands SDK Hackathon Project**  
> An AI-powered healthcare informational assistant that understands and responds in both **Tamil** and **English**, engineered with **Python**, **FastAPI**, **Jinja2 Server-Side Rendering (SSR)**, **Strands Agents SDK**, and **Google Gemini 2.0 Flash**.

---

## 🌟 Overview & Migration

The website has been migrated from a JavaScript-heavy client-side application to a robust **Python-powered FastAPI web application**. 

All user state management, language switching, form validation, emergency first-aid protocols, essential medicine cataloging, vitals trend calculations, and doctor report generations are executed by **Python backend services** and rendered server-side via **Jinja2 templates**.

### What JavaScript Was Removed vs. What Remains:
- **Removed (Over 2,400 lines of client-side JS)**:
  - ❌ Giant client-side localization dictionaries (Tamil & English translations moved to services/localization_service.py).
  - ❌ Dynamic DOM manipulation for switching navigation tabs (replaced by standard HTML routing & Jinja2 partials).
  - ❌ Client-side rendering of the 9 wound and emergency protocols (moved to services/first_aid_service.py).
  - ❌ Client-side medicine checklist filtering (moved to services/medicine_service.py).
  - ❌ Client-side localStorage vitals processing & statistics computation (moved to services/vitals_service.py).
  - ❌ Client-side Doctor Report DOM generation and mailto/WhatsApp string building (moved to outes/report.py).
- **Retained (Minimal Browser-Only APIs ~100 lines in static/js/app.js)**:
  - ✅ **Web Speech API (webkitSpeechRecognition)**: Genuinely requires browser APIs for microphone access and voice typing in Tamil (	a-IN) and English (en-US).
  - ✅ **Chart.js**: Client-side canvas library strictly for rendering interactive vitals line charts.
  - ✅ **Service Worker (static/service-worker.js)**: Required by browsers for PWA offline caching of the First-Aid Guide and static assets during network disconnection.

---

## 🏗️ Architecture & Project Structure

`
bilingual-health-assistant/
├── main.py                     # FastAPI entry point, Jinja2 config, static mounts & routes
├── routes/
│   ├── __init__.py
│   ├── views.py                # Server-rendered pages (Chat, First-Aid, Medicine Kit, Daily Log, Report)
│   ├── chat.py                 # Chat form submission & AI streaming/REST endpoints
│   ├── vitals.py               # Health log submission, deletion & data API
│   ├── report.py               # Doctor report generation, stats computation & sharing links
│   └── api.py                  # System health check & status endpoints
│
├── services/
│   ├── __init__.py
│   ├── agent_service.py        # Strands Agent SDK + Gemini integration & session memory
│   ├── tools.py                # Specialized Strands medical tools (emergency, first aid, OTC meds)
│   ├── first_aid_service.py    # 9 Emergency/Wound protocols (English & Tamil data and helpers)
│   ├── medicine_service.py     # Essential medicine catalog and filtering logic
│   ├── vitals_service.py       # Health logs JSON storage, statistics calculation, red flag analysis
│   └── localization_service.py # 100% bilingual i18n dictionary (Tamil & English) & template helpers
│
├── templates/
│   ├── base.html               # Master layout (Navbar, Status Badges, Emergency Banner, Footer)
│   ├── index.html              # Main multi-view application shell
│   ├── partials/
│   │   ├── chat_view.html          # Chat interface, suggestion chips, message history
│   │   ├── first_aid_view.html     # Offline First-Aid protocols, 4-step guide, DANGER DON'TS
│   │   ├── medicine_kit_view.html  # Essential home medicines checklist & filter categories
│   │   ├── daily_log_view.html     # Daily health check-in form & interactive vitals charts
│   │   └── doctor_report_view.html # Monthly clinical handover document & email/WhatsApp links
│   └── offline.html            # Standalone zero-dependency offline emergency first-aid page
│
├── static/
│   ├── css/
│   │   └── style.css           # Medical-teal CSS styling, responsive grid & animations
│   ├── images/
│   │   ├── icon-192.png        # PWA App Icon
│   │   └── icon-512.png        # PWA Splash Icon
│   ├── js/
│   │   └── app.js              # Minimal browser script (Speech API, Chart.js canvas, SW register)
│   ├── manifest.json           # Web app manifest for mobile & desktop installation
│   └── service-worker.js       # PWA offline cache worker for zero-internet first aid
│
├── data/
│   └── health_logs.json        # Persistent JSON database for daily vitals records
│
├── requirements.txt            # Python dependencies
├── .env.example                # Safe environment variables template
├── .env                        # Private environment variables (Gemini API key)
└── test_migration.py           # Verification test suite (12 automated tests)
`

---

## 🚀 Setup & Execution Guide

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.13)
- Google Gemini API Key ([Get a key here](https://aistudio.google.com/))

### 2. Environment Configuration
Clone the repository and set up your virtual environment:

`powershell
# Navigate to the project root directory
cd "e:\HACKATHON AWS\bilingual-health-assistant"

# Create virtual environment
python -m venv .venv

# Activate virtual environment (Windows PowerShell)
.\.venv\Scripts\Activate.ps1
# Or on Linux / macOS: source .venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
`

### 3. API Key Setup
Copy .env.example to .env and add your Google Gemini API key:
`env
GOOGLE_API_KEY=your_actual_gemini_api_key_here
`

### 4. Correct Startup Command

#### Option A: FastAPI Web Application
Launch the Python FastAPI server:
```powershell
uvicorn main:app --reload --port 8000
```
Open your browser and navigate to:
👉 **`http://127.0.0.1:8000`**

#### Option B: Streamlit Application (For Streamlit Cloud)
Launch with Streamlit:
```powershell
streamlit run streamlit_app.py
```
For **Streamlit Community Cloud** (share.streamlit.io):
- **Main file path**: `streamlit_app.py`
- Add your `GOOGLE_API_KEY` in **App Settings -> Secrets**.

---

## 🧪 Automated Verification Suite

Run the full automated test suite containing 12 unit and integration tests:

`powershell
python test_migration.py
`

All 12 test suites verify:
1. GET / (English Home Page)
2. GET /?lang=Tamil (Native Tamil Language Support)
3. GET /first-aid (Offline Emergency Protocols)
4. GET /medicine-kit (Essential Medicine Filtering)
5. GET /daily-log (Daily Health Check-in & Vitals Timeline)
6. GET /health (Backend Health Status)
7. POST /daily-log (Vitals Form Submission & Redirection)
8. POST /chat (AI & Instant Clinical Rule Engine)
9. Emergency 108 Alerting & Clinical Triage
10. POST /doctor-report/generate (Monthly Clinical Handover Generation)
11. Doctor Report View & Email / WhatsApp / PDF Sharing Links
12. Offline Standalone First-Aid Availability (static/offline.html)

---

## 🩹 Offline First-Aid Guarantee
The **First-Aid Guide** operates 100% offline without requiring an internet connection, FastAPI server, or Gemini API:
- **PWA Service Worker**: When opened once in any modern browser, static/service-worker.js caches the emergency guide and styles.
- **Standalone Offline Document**: Opening static/offline.html directly in any web browser provides instant step-by-step guidance for severe arterial bleeding, burns, venomous snakebites, animal bites, and CPR resuscitation with emergency 108 dialing.

---

## 🛡️ Medical Disclaimer
HealthMate AI is designed for preliminary guidance, remote community support, and educational purposes. It does not replace a licensed medical practitioner and does not issue clinical diagnoses or prescriptions. In emergencies, call **108** or proceed immediately to the nearest Primary Health Center (PHC).
