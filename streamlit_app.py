"""
HealthMate AI — Streamlit Application Entrypoint
Provides a full-featured Streamlit Cloud deployment option for HealthMate AI.
Main file path for Streamlit Cloud: streamlit_app.py
"""

import os
import urllib.parse
from datetime import datetime
import streamlit as st

# Configure Streamlit page
st.set_page_config(
    page_title="HealthMate AI — Bilingual Health Assistant",
    page_icon="✚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import backend services
from services.localization_service import get_translations
from services.first_aid_service import get_wound_protocol, get_all_wound_keys, WOUND_PROTOCOLS
from services.medicine_service import get_medicines
from services.vitals_service import (
    get_patient_logs,
    save_health_log,
    compute_vitals_statistics,
    delete_health_log
)
from services.agent_service import run_health_agent, summarize_doctor_report

# Custom styling matching HealthMate medical-teal branding
st.markdown("""
<style>
    :root {
        --primary: #0a8a6b;
    }
    .main-header {
        background: linear-gradient(135deg, #0a8a6b 0%, #065f46 100%);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2rem;
    }
    .main-header p {
        color: #d1fae5;
        margin-top: 0.25rem;
        font-size: 1rem;
    }
    .emergency-box {
        background-color: #fef2f2;
        border: 2px solid #ef4444;
        border-radius: 10px;
        padding: 1rem 1.25rem;
        margin-bottom: 1.5rem;
        color: #991b1b;
    }
    .step-box {
        background-color: #f0fdf4;
        border-left: 4px solid #0a8a6b;
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
        border-radius: 0 8px 8px 0;
    }
    .dont-box {
        background-color: #fff1f2;
        border-left: 4px solid #f43f5e;
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
        border-radius: 0 8px 8px 0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Controls
with st.sidebar:
    st.markdown("### 🌐 Language / மொழி")
    selected_language = st.radio(
        "Select Response Language:",
        options=["English", "Tamil"],
        index=0,
        format_func=lambda x: "English" if x == "English" else "தமிழ் (Tamil)",
        label_visibility="collapsed"
    )
    is_tamil = selected_language == "Tamil"
    i18n = get_translations(selected_language)

    st.markdown("---")
    st.markdown("### 🚨 Emergency Helpline")
    st.error("**India Ambulance: 108**\n\nImmediate medical triage for severe bleeding, chest pain, stroke, or breathing failure.")

    st.markdown("---")
    st.markdown("### ℹ️ About HealthMate AI")
    st.caption("Engineered with **Python**, **Strands Agents SDK**, and **Google Gemini 2.0 Flash** for rural and remote communities.")

# Banner Header
st.markdown(f"""
<div class="main-header">
    <h1>✚ HealthMate AI</h1>
    <p>{i18n['brandTagline']}</p>
</div>
""", unsafe_allow_html=True)

# Top Navigation Tabs
tab_chat, tab_firstaid, tab_meds, tab_vitals, tab_report = st.tabs([
    i18n['tabChat'],
    i18n['tabWounds'],
    i18n['tabMeds'],
    i18n['tabChart'],
    i18n['tabReport']
])

# ==============================================================================
# TAB 1: BILINGUAL AI CHAT ASSISTANT
# ==============================================================================
with tab_chat:
    st.subheader(i18n['heroTitle'])
    st.caption(i18n['heroSubtitle'])

    # Suggestion Chips
    st.markdown(f"**{i18n['suggestLabel']}**")
    cols = st.columns(len(i18n['suggestions']))
    for idx, sug in enumerate(i18n['suggestions']):
        if cols[idx].button(sug[:28] + "...", key=f"sug_{idx}", help=sug):
            st.session_state["user_chat_input"] = sug

    # Initialize chat session state
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # Display past conversation
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "✚"):
            st.markdown(msg["text"])

    # Chat Input
    default_input = st.session_state.pop("user_chat_input", "")
    user_query = st.chat_input(placeholder=i18n['chatPlaceholder']) or default_input

    if user_query:
        st.session_state.chat_messages.append({"role": "user", "text": user_query})
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_query)

        with st.chat_message("assistant", avatar="✚"):
            with st.spinner("AI analyzing symptoms..." if not is_tamil else "AI அறிகுறிகளை ஆராய்கிறது..."):
                reply, is_emergency = run_health_agent(
                    message=user_query,
                    language=selected_language,
                    session_id="streamlit_session"
                )
                if is_emergency:
                    st.markdown("""
                    <div class="emergency-box">
                        <strong>🚨 CRITICAL MEDICAL EMERGENCY DETECTED</strong><br>
                        Please call <strong>108</strong> or proceed to the nearest emergency department immediately!
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown(reply)
                st.session_state.chat_messages.append({"role": "assistant", "text": reply})

# ==============================================================================
# TAB 2: OFFLINE FIRST-AID EMERGENCY GUIDE
# ==============================================================================
with tab_firstaid:
    st.subheader(i18n['woundsTitle'])
    st.caption(i18n['woundsDesc'])

    wound_keys = get_all_wound_keys()
    wound_options = {k: i18n['woundPills'].get(k, k) for k in wound_keys}

    selected_wound_key = st.selectbox(
        i18n['woundsSelectLabel'],
        options=wound_keys,
        format_func=lambda k: wound_options[k]
    )

    protocol = get_wound_protocol(selected_wound_key, selected_language)

    st.markdown(f"### {protocol['title']}")
    st.info(f"**Severity Level:** {protocol['severity']}")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"<div class='step-box'><strong>Step 1:</strong><br>{protocol['step1']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='step-box'><strong>Step 2:</strong><br>{protocol['step2']}</div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='step-box'><strong>Step 3:</strong><br>{protocol['step3']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='step-box'><strong>Step 4:</strong><br>{protocol['step4']}</div>", unsafe_allow_html=True)

    st.markdown(f"#### 🚫 {'தவிர்க்க வேண்டிய ஆபத்தான செயல்கள்:' if is_tamil else 'CRITICAL DANGER: What You Must NEVER Do:'}")
    for dont in protocol['donts']:
        st.markdown(f"<div class='dont-box'>❌ {dont}</div>", unsafe_allow_html=True)

    st.warning(f"**🚑 {'மருத்துவமனை செல்லுதல்:' if is_tamil else 'Hospital / PHC Transport Advisory:'}** {protocol['transport']}")

# ==============================================================================
# TAB 3: ESSENTIAL HOME MEDICINE KIT
# ==============================================================================
with tab_meds:
    st.subheader(i18n['medsTitle'])
    st.caption(i18n['medsDesc'])

    cat_options = list(i18n['medFilters'].keys())
    selected_cat = st.segmented_control(
        "Category Filter",
        options=cat_options,
        default="all",
        format_func=lambda c: i18n['medFilters'][c],
        label_visibility="collapsed"
    ) or "all"

    meds = get_medicines(category=selected_cat, lang=selected_language)

    m_cols = st.columns(2)
    for idx, med in enumerate(meds):
        with m_cols[idx % 2]:
            with st.container(border=True):
                st.markdown(f"### {med['icon']} {med['name']}")
                st.caption(f"**Type:** {med['type']}")
                st.markdown(f"**Usage / Method:** {med['dose']}")
                st.markdown(f"**Dosage Limit:** {med['limit']}")
                st.warning(f"⚠️ {med['caution']}")

# ==============================================================================
# TAB 4: DAILY HEALTH CHECK-IN & VITALS TRACKER
# ==============================================================================
with tab_vitals:
    st.subheader(i18n['chartSectionTitle'])
    st.caption(i18n['chartSectionDesc'])

    with st.expander(f"➕ {i18n['logFormTitle']}", expanded=True):
        with st.form("daily_vitals_form", clear_on_submit=True):
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                v_date = st.date_input(i18n['lblDate'], value=datetime.now())
                v_sys = st.number_input(i18n['lblSysBp'], min_value=60, max_value=250, value=120)
                v_sugar = st.number_input(i18n['lblSugar'], min_value=40, max_value=600, value=100)
                v_spo2 = st.number_input(i18n['lblSpo2'], min_value=50, max_value=100, value=98)
            with f_col2:
                v_time = st.time_input(i18n['lblTime'], value=datetime.now().time())
                v_dia = st.number_input(i18n['lblDiaBp'], min_value=40, max_value=150, value=80)
                v_pulse = st.number_input(i18n['lblPulse'], min_value=40, max_value=220, value=72)
                v_temp = st.number_input(i18n['lblTemp'], min_value=90.0, max_value=108.0, value=98.6, step=0.1)

            v_pain = st.slider(i18n['lblPain'], 0, 10, 0)
            v_symptoms = st.multiselect(
                i18n['lblSymptomsSelect'],
                options=list(i18n['symptomsDict'].keys()),
                format_func=lambda s: i18n['symptomsDict'][s]
            )
            v_severity = st.selectbox(
                i18n['lblSeverity'],
                options=["Mild", "Moderate", "Severe"],
                format_func=lambda s: i18n['severityOptions'][s]
            )
            v_notes = st.text_input(i18n['lblNotes'], placeholder=i18n['phNotes'])

            submit_vitals = st.form_submit_button(i18n['saveLogBtn'], use_container_width=True)
            if submit_vitals:
                entry = {
                    "id": f"log_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
                    "patient_id": "default",
                    "date": str(v_date),
                    "time": v_time.strftime("%H:%M"),
                    "systolic_bp": int(v_sys),
                    "diastolic_bp": int(v_dia),
                    "blood_glucose": int(v_sugar),
                    "heart_rate": int(v_pulse),
                    "spo2": int(v_spo2),
                    "temperature": float(v_temp),
                    "pain_level": int(v_pain),
                    "symptoms": v_symptoms,
                    "condition_severity": v_severity,
                    "notes": v_notes.strip()
                }
                save_health_log(entry)
                st.success("✓ Daily vitals entry saved successfully!")
                st.rerun()

    # Vitals Progression Charts
    logs = get_patient_logs("default")
    if logs:
        import pandas as pd
        df = pd.DataFrame(logs)
        df["datetime"] = df["date"] + " " + df["time"]
        df = df.sort_values("datetime")

        st.markdown(f"### {i18n['chartsTitle']}")
        chart_choice = st.radio(
            "Select Metric View:",
            options=["Blood Pressure", "Sugar & Temperature", "Pulse & Oxygen SpO2"],
            horizontal=True
        )

        if chart_choice == "Blood Pressure":
            st.line_chart(df.set_index("date")[["systolic_bp", "diastolic_bp"]])
        elif chart_choice == "Sugar & Temperature":
            st.line_chart(df.set_index("date")[["blood_glucose", "temperature"]])
        else:
            st.line_chart(df.set_index("date")[["heart_rate", "spo2"]])

        # History Timeline Cards
        st.markdown(f"### {i18n['timelineTitle']}")
        for item in logs[:10]:
            with st.container(border=True):
                t_col1, t_col2 = st.columns([4, 1])
                with t_col1:
                    st.markdown(f"**📅 {item['date']} • {item['time']}** | *Severity:* `{item['condition_severity']}`")
                    st.write(f"BP: **{item.get('systolic_bp')}/{item.get('diastolic_bp')}** | Sugar: **{item.get('blood_glucose')} mg/dL** | SpO2: **{item.get('spo2')}%** | Pulse: **{item.get('heart_rate')} BPM** | Temp: **{item.get('temperature')}°F**")
                    if item.get("symptoms"):
                        st.caption(f"Symptoms: {', '.join([i18n['symptomsDict'].get(s, s) for s in item['symptoms']])}")
                    if item.get("notes"):
                        st.caption(f"Notes: {item['notes']}")
                with t_col2:
                    if st.button("🗑️ Delete", key=f"del_{item['id']}"):
                        delete_health_log(item['id'])
                        st.rerun()

# ==============================================================================
# TAB 5: MONTHLY DOCTOR REPORT & TELE-SHARE
# ==============================================================================
with tab_report:
    st.subheader(i18n['reportTitle'])
    st.caption(i18n['reportDesc'])

    r_col1, r_col2 = st.columns(2)
    with r_col1:
        p_name = st.text_input(i18n['lblPatName'], value="Ramesh Kumar" if not is_tamil else "ரமேஷ் குமார்")
        d_email = st.text_input(i18n['lblDocEmail'], placeholder="doctor@clinic.com")
    with r_col2:
        p_age = st.text_input(i18n['lblPatAge'], value="48 Y / Male" if not is_tamil else "48 வயது / ஆண்")
        d_phone = st.text_input(i18n['lblDocPhone'], placeholder="919876543210")

    if st.button(i18n['generateReportBtn'], type="primary", use_container_width=True):
        patient_logs = get_patient_logs("default")
        stats = compute_vitals_statistics(patient_logs)

        vitals_text = (
            f"Patient: {p_name} ({p_age})\n"
            f"Total Days Logged: {stats['total_days_logged']}\n"
            f"BP Averages: {stats['avg_systolic_bp']}/{stats['avg_diastolic_bp']} mmHg (Peak: {stats['max_bp']})\n"
            f"Blood Sugar: Avg {stats['avg_blood_glucose']} mg/dL (Peak: {stats['max_glucose']} mg/dL)\n"
            f"SpO2: Avg {stats['avg_spo2']}% (Lowest: {stats['min_spo2']}%)\n"
            f"Pulse: Avg {stats['avg_pulse']} BPM\n"
            f"Temperature: Avg {stats['avg_temp']}°F\n"
            f"Red Flags: {', '.join(stats['red_flags']) if stats['red_flags'] else 'None'}"
        )

        with st.spinner("Generating clinical physician handover summary with Gemini..."):
            clinical_memo = summarize_doctor_report(vitals_text, selected_language)

        with st.container(border=True):
            st.markdown(f"## ✚ {i18n['docTitle']}")
            st.caption(i18n['docSubtitle'])
            st.markdown("---")

            m_col1, m_col2 = st.columns(2)
            with m_col1:
                st.write(f"**{i18n['docLblName']}** {p_name}")
                st.write(f"**{i18n['docLblDemo']}** {p_age}")
            with m_col2:
                st.write(f"**{i18n['docLblLoc']}** Remote / Hospital > 30 km")
                st.write(f"**{i18n['docLblWin']}** Past 30 Days")

            st.markdown(f"### {i18n['docSec1Title']}")
            s1, s2, s3, s4 = st.columns(4)
            s1.metric(i18n['statAvgBp'], f"{stats['avg_systolic_bp']}/{stats['avg_diastolic_bp']}" if stats['avg_systolic_bp'] else "--")
            s2.metric(i18n['statAvgSugar'], f"{stats['avg_blood_glucose']} mg/dL" if stats['avg_blood_glucose'] else "--")
            s3.metric(i18n['statAvgSpo2'], f"{stats['avg_spo2']}%" if stats['avg_spo2'] else "--")
            s4.metric(i18n['statAvgPulse'], f"{stats['avg_pulse']} BPM" if stats['avg_pulse'] else "--")

            st.markdown(f"### {i18n['docSec2Title']}")
            if stats['red_flags']:
                for rf in stats['red_flags']:
                    st.error(f"⚠️ {rf}")
            else:
                st.success("🟢 No acute threshold abnormalities logged.")

            st.markdown(f"### {i18n['docSec4Title']}")
            st.info(clinical_memo)

            # Share Links
            mail_subj = urllib.parse.quote(f"Monthly Vitals Report: {p_name}")
            mail_body = urllib.parse.quote(f"Patient: {p_name}\n\nClinical Summary:\n{clinical_memo}")
            wa_text = urllib.parse.quote(f"*HealthMate AI Report: {p_name}*\n\n{clinical_memo}")

            c_mail, c_wa = st.columns(2)
            c_mail.markdown(f"[✉️ **Email to Doctor**](mailto:{d_email}?subject={mail_subj}&body={mail_body})")
            c_wa.markdown(f"[💬 **Send via WhatsApp**](https://api.whatsapp.com/send?phone={d_phone}&text={wa_text})")

# Medical Disclaimer Footer
st.markdown("---")
st.caption(f"⚠️ **{i18n['disclaimerHeader']}**: {i18n['disclaimerBody']}")
st.caption(f"🏆 {i18n['hackathonFooter']}")
