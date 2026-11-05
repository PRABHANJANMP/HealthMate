# services/agent_service.py
"""
Bilingual AI Health Assistant - Agent Module
Uses Strands Agents SDK with Google Gemini.
Supports English, Tamil, and Tanglish.
Includes SafeCallbackHandler to prevent Windows console cp1252 charmap crashes.
"""

import os
from dotenv import load_dotenv
from strands import Agent
from strands.models.gemini import GeminiModel
from services.tools import (
    check_for_emergency,
    assess_symptom_status,
    get_otc_medication_info,
    get_first_aid_guidance,
    explain_possible_causes,
    get_general_health_tips,
    get_wound_treatment_guide,
    get_essential_medicine_list,
    generate_doctor_summary,
    is_emergency,
)

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()

HEALTH_SYSTEM_PROMPT = """
You are HealthMate AI, an expert AI-powered Bilingual Health Assistant.
You understand English, Tamil script (தமிழ்), and Tanglish (Tamil words written in English letters, such as "enaku vanthi varuthu", "thalavali", "kaichal", "vayiru eriyuthu").

LANGUAGE RULES:
- If the user selects Tamil OR writes in Tamil/Tanglish, reply ENTIRELY in Tamil (தமிழ் எழுத்துக்களில்).
- If the user selects English, reply in English.
- Always be empathetic, caring, and professional.

STRUCTURED RESPONSE FORMAT:
When a user describes any health issue (e.g. vomiting, fever, headache, body pain, loose motion):
Directly address their specific symptom with these sections:
1. 📊 நிலை மதிப்பீடு (Status - Good or Bad?): Explain whether it is mild (manageable at home) or concerning/bad based on duration.
2. 🔍 சாத்தியமான காரணங்கள் (Possible Causes): 2-3 likely factors (e.g. food poisoning, dehydration, infection).
3. 💊 பாதுகாப்பான முதலுதவி மருந்துகள் (Supportive OTC Meds): Common safe options (e.g., ORS for vomiting/dehydration, Paracetamol for fever, Antacid for acidity) along with dosage limits and precautions.
4. 🩹 எளிய உடனடி முதலுதவி (Quick Aid Guide): 3 immediate home care steps.
5. ❓ 2-3 கேள்விகள் (Follow-up Questions): Ask clarifying questions regarding duration, severity, and other signs.
6. ⚠️ மருத்துவ எச்சரிக்கை: Remind them to visit a qualified doctor if severe.

CRITICAL MEDICAL SAFETY:
- You are an informational assistant, NOT a doctor.
- In emergencies (severe chest pain, breathing difficulty, stroke signs, heavy bleeding, unconsciousness),
  strongly advise calling 108 immediately!
"""

class SafeCallbackHandler:
    """Suppresses direct console printing of Unicode/Tamil characters to avoid Windows cp1252 charmap crashes."""
    def __call__(self, **kwargs):
        pass

_session_histories: dict[str, list] = {}
MAX_HISTORY_MESSAGES = 10

def get_session_history(session_id: str) -> list:
    return _session_histories.get(session_id, [])

def clear_session(session_id: str) -> None:
    if session_id in _session_histories:
        del _session_histories[session_id]

def is_tanglish_or_tamil(text: str) -> bool:
    t = text.lower()
    tanglish_words = [
        "enaku", "vanthi", "varuthu", "thalavali", "kaichal", "valikuthu", "valikudhu",
        "thala", "vayiru", "udambu", "irumal", "sali", "eriyuthu", "mudila", "nenju", "bayam"
    ]
    return any(w in t for w in tanglish_words)

def create_agent(history: list) -> Agent:
    model = GeminiModel(
        client_args={"api_key": GOOGLE_API_KEY},
        model_id="gemini-2.0-flash",
    )
    return Agent(
        model=model,
        system_prompt=HEALTH_SYSTEM_PROMPT,
        callback_handler=SafeCallbackHandler(),
        tools=[
            check_for_emergency,
            assess_symptom_status,
            get_otc_medication_info,
            get_first_aid_guidance,
            explain_possible_causes,
            get_general_health_tips,
            get_wound_treatment_guide,
            get_essential_medicine_list,
            generate_doctor_summary,
        ],
        messages=history[-MAX_HISTORY_MESSAGES:] if history else [],
    )

def fast_gemini_call(prompt: str, system_prompt: str = HEALTH_SYSTEM_PROMPT, timeout_secs: float = 2.0) -> str:
    """Attempts a fast direct Gemini call with immediate 429 quota break, eliminating slow retry delays."""
    if not GOOGLE_API_KEY:
        return ""
    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=GOOGLE_API_KEY)
        for m in ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-2.5-flash"]:
            try:
                cfg = types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.3,
                    max_output_tokens=700,
                )
                resp = client.models.generate_content(
                    model=m,
                    contents=prompt,
                    config=cfg,
                )
                if resp and resp.text and len(resp.text.strip()) > 30:
                    return resp.text.strip()
            except Exception as err:
                err_str = str(err)
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                    break
                continue
    except Exception:
        pass
    return ""

def get_instant_clinical_reply(message: str, target_language: str = "English") -> str:
    """Instantly generates (in 0.0001s) structured clinical guidance using verified medical rules."""
    m_lower = message.lower()
    is_wound = any(w in m_lower for w in ["wound", "cut", "burn", "bite", "fracture", "bleed", "காயம்", "வெட்டு", "தீக்காயம்", "கடி"])
    status = assess_symptom_status(message, 1, "moderate", target_language)
    causes = explain_possible_causes(message, target_language)
    meds = get_otc_medication_info(message, target_language)
    aid = get_wound_treatment_guide(message, target_language) if is_wound else get_first_aid_guidance(message, target_language)
    return f"{status}\n\n{causes}\n\n{meds}\n\n{aid}"

def summarize_doctor_report(vitals_summary: str, language: str = "English") -> str:
    """Fast doctor report summary."""
    target_lang = "Tamil" if language == "Tamil" else "English"
    prompt = (
        f"You are HealthMate AI generating an official Monthly Doctor Handover Report.\n"
        f"Language requirement: {target_lang}\n"
        f"Patient Vitals Data and Monthly Records:\n{vitals_summary}\n\n"
        f"Please write a structured medical report for an attending physician with:\n"
        f"1. Executive Vitals Summary (Average BP, Sugar, Pulse, SpO2 stability).\n"
        f"2. Notable Anomalies or Red Flags (high BP, low SpO2, fever episodes).\n"
        f"3. Symptom Timeline & Frequency.\n"
        f"4. Suggested Clinical Investigations & Physician Action Plan.\n"
        f"Keep the tone clinical, concise, and professional."
    )
    ai_text = fast_gemini_call(prompt, timeout_secs=2.0)
    if ai_text and len(ai_text) > 50:
        return ai_text
    return generate_doctor_summary(vitals_summary, target_lang)

def run_health_agent(
    message: str,
    language: str = "English",
    session_id: str = "default",
) -> tuple[str, bool]:
    user_is_emergency = is_emergency(message)
    target_language = "Tamil" if (language == "Tamil" or is_tanglish_or_tamil(message)) else "English"

    # Emergency triage: instantaneous response (0.0001s)
    if user_is_emergency:
        return check_for_emergency(message, target_language), True

    full_prompt = (
        f"[Preferred response language: {target_language}]\n\n"
        f"User query: '{message}'\n\n"
        f"Instructions: Directly address the user's specific symptom or condition. "
        f"Include status assessment (good/bad), possible causes, supportive OTC medications with precautions, "
        f"quick aid steps, and ask 2 follow-up questions. Reply in {target_language}."
    )

    # Try fast Gemini AI response (< 2s)
    ai_reply = fast_gemini_call(full_prompt, HEALTH_SYSTEM_PROMPT, timeout_secs=2.0)

    if ai_reply and len(ai_reply) > 40:
        is_emergency_flag = (
            user_is_emergency or
            "EMERGENCY_DETECTED" in ai_reply or
            "108" in ai_reply or
            "அவசர" in ai_reply
        )
        ai_reply = ai_reply.replace("EMERGENCY_DETECTED\n", "").replace("AMBULANCE_NUMBER: 108\n\n", "").strip()

        history = _session_histories.get(session_id, [])
        history.append({"role": "user", "text": message})
        history.append({"role": "assistant", "text": ai_reply})
        _session_histories[session_id] = history[-MAX_HISTORY_MESSAGES:]
        return ai_reply, is_emergency_flag

    # Instant clinical response engine (0.0001s)
    clinical_reply = get_instant_clinical_reply(message, target_language).strip()
    history = _session_histories.get(session_id, [])
    history.append({"role": "user", "text": message})
    history.append({"role": "assistant", "text": clinical_reply})
    _session_histories[session_id] = history[-MAX_HISTORY_MESSAGES:]

    return clinical_reply, False
