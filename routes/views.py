# routes/views.py
"""
Server-Rendered Views & Navigation Routes (Jinja2)
"""

import urllib.parse
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Request, Query, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from services.localization_service import get_translations
from services.first_aid_service import get_wound_protocol, get_all_wound_keys, WOUND_PROTOCOLS
from services.medicine_service import get_medicines
from services.vitals_service import get_patient_logs, compute_vitals_statistics
from services.agent_service import get_session_history, clear_session
from routes.report import build_report_data

router = APIRouter(tags=["Views"])

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def home_page(
    request: Request,
    tab: Optional[str] = Query(default="chat"),
    lang: Optional[str] = Query(default=None),
    wound: Optional[str] = Query(default="severe-bleeding"),
    category: Optional[str] = Query(default="all"),
    report_ready: Optional[str] = Query(default=None),
    p_name: Optional[str] = Query(default=None),
    p_age: Optional[str] = Query(default=None),
    d_email: Optional[str] = Query(default=None),
    d_phone: Optional[str] = Query(default=None),
    saved: Optional[str] = Query(default=None),
):
    # Determine language preference from query or cookie
    if lang in ("Tamil", "ta"):
        selected_lang = "Tamil"
    elif lang in ("English", "en"):
        selected_lang = "English"
    else:
        cookie_lang = request.cookies.get("healthmate_lang", "English")
        selected_lang = "Tamil" if cookie_lang == "Tamil" else "English"

    # Session ID
    session_id = request.cookies.get("healthmate_session_id")
    if not session_id:
        session_id = f"sess_{int(datetime.now().timestamp())}"

    dict_i18n = get_translations(selected_lang)

    # Wound protocols
    all_wound_keys = get_all_wound_keys()
    active_wound_key = wound if wound in WOUND_PROTOCOLS else "severe-bleeding"
    active_protocol = get_wound_protocol(active_wound_key, selected_lang)

    # Medicines
    medicines = get_medicines(category=category, lang=selected_lang)

    # Vitals & Stats
    logs = get_patient_logs("default")
    stats = compute_vitals_statistics(logs)

    # Chat history
    chat_history = get_session_history(session_id)

    # Doctor report (if requested)
    report_data = None
    if report_ready or tab == "report":
        patient_name = p_name or "Ramesh Kumar"
        patient_age = p_age or ("48 Y / Male" if selected_lang == "English" else "48 வயது / ஆண்")
        doctor_email = d_email or ""
        doctor_phone = d_phone or ""
        if report_ready:
            report_data = build_report_data(patient_name, patient_age, doctor_email, doctor_phone, selected_lang)

    # Check for emergency alert in session
    is_emergency = any("108" in (msg.get("text", "")) or "அவசர" in (msg.get("text", "")) for msg in chat_history)

    response = templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "active_tab": tab or "chat",
            "lang": selected_lang,
            "is_tamil": selected_lang == "Tamil",
            "i18n": dict_i18n,
            "active_wound_key": active_wound_key,
            "all_wound_keys": all_wound_keys,
            "active_protocol": active_protocol,
            "active_category": category or "all",
            "medicines": medicines,
            "vitals_logs": logs,
            "vitals_stats": stats,
            "session_id": session_id,
            "chat_history": chat_history,
            "report_data": report_data,
            "p_name": p_name or "",
            "p_age": p_age or "",
            "d_email": d_email or "",
            "d_phone": d_phone or "",
            "is_emergency": is_emergency,
            "saved": bool(saved),
        }
    )

    response.set_cookie("healthmate_lang", selected_lang, max_age=86400 * 30)
    response.set_cookie("healthmate_session_id", session_id, max_age=86400 * 30)
    return response

@router.get("/first-aid")
def view_first_aid(request: Request, wound: Optional[str] = None, lang: Optional[str] = None):
    url = f"/?tab=wounds"
    if wound:
        url += f"&wound={wound}"
    if lang:
        url += f"&lang={lang}"
    return RedirectResponse(url=url, status_code=303)

@router.get("/medicine-kit")
def view_medicine_kit(request: Request, category: Optional[str] = None, lang: Optional[str] = None):
    url = f"/?tab=meds"
    if category:
        url += f"&category={category}"
    if lang:
        url += f"&lang={lang}"
    return RedirectResponse(url=url, status_code=303)

@router.get("/daily-log")
def view_daily_log(request: Request, lang: Optional[str] = None):
    url = f"/?tab=chart"
    if lang:
        url += f"&lang={lang}"
    return RedirectResponse(url=url, status_code=303)

@router.get("/doctor-report")
def view_doctor_report(request: Request, lang: Optional[str] = None):
    url = f"/?tab=report"
    if lang:
        url += f"&lang={lang}"
    return RedirectResponse(url=url, status_code=303)

@router.post("/set-language")
def set_language(request: Request, language: str = Form(...), redirect_url: Optional[str] = Form(default="/")):
    selected_lang = "Tamil" if language in ("Tamil", "ta") else "English"
    target = redirect_url or "/"
    # Replace or append lang query parameter
    parsed = urllib.parse.urlparse(target)
    query_params = urllib.parse.parse_qs(parsed.query)
    query_params["lang"] = [selected_lang]
    new_query = urllib.parse.urlencode(query_params, doseq=True)
    new_url = urllib.parse.urlunparse(parsed._replace(query=new_query))

    response = RedirectResponse(url=new_url, status_code=303)
    response.set_cookie("healthmate_lang", selected_lang, max_age=86400 * 30)
    return response

@router.post("/clear-session")
def clear_session_form(request: Request):
    session_id = request.cookies.get("healthmate_session_id", "default")
    clear_session(session_id)
    lang = request.cookies.get("healthmate_lang", "English")
    return RedirectResponse(url=f"/?tab=chat&lang={lang}", status_code=303)
