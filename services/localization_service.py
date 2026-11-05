# services/localization_service.py
"""
Localization & Internationalization (i18n) Service
Provides 100% complete bilingual translation dictionaries (English & Tamil).
"""

TRANSLATIONS = {
    "English": {
        # Navigation Tabs
        "tabChat": "💬 Chat",
        "tabWounds": "🩹 Offline First-Aid",
        "tabMeds": "🛒 Medicine Kit",
        "tabChart": "📊 Daily Log & Chart",
        "tabReport": "📄 Doctor Report",

        # Header & Banners
        "brandTagline": "Remote Emergency & Bilingual Health Assistant • தமிழ் / English",
        "statusReady": "AI Ready",
        "statusConnecting": "Connecting...",
        "networkOnline": "Online",
        "networkOffline": "Offline Mode",
        "cacheReady": "Offline Pack: Ready",
        "clearBtnTitle": "Clear Chat History",
        "dailyBannerTitle": "Daily Health Check-in: How are you feeling today?",
        "dailyBannerDesc": "Living far from a hospital? Regularly record your blood pressure, sugar, and symptoms to build your monthly doctor report.",
        "quickCheckinBtn": "➕ Log Today's Vitals",
        "emergencyTitle": "Medical Emergency Notice",
        "emergencyDesc": "If you or someone else is experiencing severe chest pain, breathing difficulty, heavy blood loss, or unconsciousness, call 108 (India) or rush to the nearest Primary Health Center (PHC) immediately.",
        "emergencyBtn": "Call 108 📞",

        # Offline Banner & Triage
        "offlineBannerTitle": "Offline Mode Active • Internet Disconnected",
        "offlineBannerDesc": "You are currently offline. Live AI consultation is unavailable without internet, but your cached Offline First-Aid Guide and saved vitals records are 100% available locally.",
        "offlineBtnText": "🩹 Open Offline First-Aid",
        "offlineGuideStatus": "Offline First-Aid Pack: 100% Downloaded & Saved in Browser Cache Storage",
        "triageTitle": "CRITICAL EMERGENCY NOTICE: When to Seek Immediate Hospital / 108 Care",
        "triageSubtitle": "First-aid guidance stabilizes the victim and prevents death while transport is arranged. It NEVER replaces professional hospital emergency care, surgery, or antivenom administration.",
        "triageRushTitle": "🚑 Call 108 / Rush to Nearest Hospital Immediately If:",
        "triageRoleTitle": "🛡️ How to Use This Offline Guide:",
        "triageRoleDesc": "When you are in a remote village, highway, or facing power/network failure: Select the injury type below. Follow the 4-step clinical protocol, heed the DANGER DON'TS, and safely transport the patient to the nearest Primary Health Center (PHC).",
        "triageRushList": [
            "Pumping arterial or heavy bleeding that does not stop with direct palm pressure",
            "Victim is unresponsive, unconscious, or stopped breathing (start CPR immediately)",
            "Any venomous snakebite (Anti-Snake Venom required in hospital within 1-2 hours)",
            "Severe burns larger than a palm, electrical burns, or burns on face, neck, or groin",
            "Suspected broken neck, spine, or thigh bone (femur) — keep victim completely still",
            "Dog or wild animal bite (requires Anti-Rabies Vaccine & Immunoglobulin within 24 hours)"
        ],

        # View 1: Chat
        "hackathonTag": "Remote Care Healthcare AI • Strands SDK & Gemini",
        "heroTitle": "Your Health, Guided in Your Language.",
        "heroSubtitle": "Triage symptoms, understand emergency wound care, get verified OTC home remedies, and track vitals when hospitals are hours away.",
        "suggestLabel": "💡 Suggested Inquiries:",
        "chatTitle": "Health Consultation Session",
        "chatSubtitle": "Informational AI guidance • Not a clinical diagnosis",
        "voiceLabel": "Voice Input",
        "voiceListening": "Listening...",
        "welcomeHtml": "<strong>Hello! I am HealthMate AI. 👋</strong><br><br>I am your remote healthcare guide. I can help with <strong>emergency wound treatment</strong>, recommended <strong>essential home medicines</strong>, daily <strong>vitals tracking</strong>, and preparing a <strong>monthly report for your doctor</strong> in <strong>English</strong> or <strong>Tamil</strong>.<br><br><em>How can I assist your health or family today?</em>",
        "chatPlaceholder": "Describe symptoms, wounds, or ask health questions in English or தமிழ்...",
        "sendText": "Send",
        "privacyNote": "🔒 Private & secure: Confidential consultation notes for remote communities.",
        "chatOfflineWarning": "⚠️ **Offline Mode Active: Live AI Consultation is Unavailable Without Internet.**<br><br>Your device is currently disconnected. Live AI consultation cannot reach the server, but your complete **Offline First-Aid Guide** is ready and saved locally.<br><br>👉 Please open the <strong>[🩹 Offline First-Aid]</strong> tab to view step-by-step instructions for cuts, severe bleeding, burns, fractures, snakebites, animal bites, and unconsciousness/CPR.<br><br><em>In an acute emergency, call <strong>108</strong> immediately.</em>",

        # View 2: Offline First-Aid Tutorial
        "woundsTitle": "Complete Offline Emergency First-Aid Guide",
        "woundsDesc": "Clinically verified, step-by-step first-aid protocols for remote areas, villages, and emergencies when hospital or ambulance is hours away. Fully functional offline.",
        "woundsSelectLabel": "Select First-Aid / Emergency Condition:",
        "woundPills": {
            "severe-bleeding": "🚨 Severe Bleeding & Tourniquet",
            "minor-cuts": "🩹 Minor Cuts & Bleeding",
            "burns": "🔥 Burns (1st to 3rd Degree)",
            "fractures": "🦴 Broken Bones & Splints",
            "snakebites": "🐍 Snakebites (Anti-Venom Protocol)",
            "animal-bites": "🐕 Dog & Animal Bites (Rabies)",
            "unconsciousness": "🫀 Unconsciousness & CPR (DRSABCD)",
            "puncture-wounds": "🔩 Puncture & Rusty Nails (Tetanus)",
            "sepsis": "⚠️ Sepsis & Infection Signs"
        },

        # View 3: Medicine Kit
        "medsTitle": "Essential Home Medicine & First-Aid Kit Checklist",
        "medsDesc": "Verified list of vital OTC medicines and diagnostic devices to buy and stock at home in areas with limited pharmacies or medical centers.",
        "medFilters": {
            "all": "All Supplies",
            "wound": "🩹 Wound & Antiseptics",
            "fever": "🌡️ Fever & Pain",
            "stomach": "🤢 Stomach & ORS",
            "allergy": "🐝 Allergies & Burns",
            "tools": "🩺 Vital Devices"
        },
        "copyMedsBtn": "📋 Copy Shopping List",
        "printMedsBtn": "🖨️ Print List",

        # View 4: Daily Log & Chart
        "chartSectionTitle": "Daily Health Check-in & Vitals Tracker",
        "chartSectionDesc": "Record your daily health metrics (BP, blood sugar, SpO2, temperature, symptoms). Visual trend graphs help you and your visiting doctor detect problems early.",
        "logFormTitle": "☀️ Daily Health Check-in Entry",
        "lblDate": "Date:",
        "lblTime": "Time of Measurement:",
        "lblSysBp": "Systolic BP (High / mmHg):",
        "lblDiaBp": "Diastolic BP (Low / mmHg):",
        "lblSugar": "Blood Sugar (mg/dL):",
        "lblPulse": "Heart Rate / Pulse (BPM):",
        "lblSpo2": "Oxygen SpO2 (%):",
        "lblTemp": "Temperature (°F):",
        "lblPain": "Pain Severity (0 = None, 10 = Severe):",
        "lblSymptomsSelect": "Select Any Symptoms Experienced Today:",
        "lblSeverity": "Overall Feeling Today:",
        "lblNotes": "Notes / Food / Meds Taken:",
        "phSysBp": "e.g. 120",
        "phDiaBp": "e.g. 80",
        "phSugar": "e.g. 95 (Fasting) or 130",
        "phPulse": "e.g. 72",
        "phSpo2": "e.g. 98",
        "phTemp": "e.g. 98.6",
        "phNotes": "e.g. Took Paracetamol, rested well, drank ORS...",
        "severityOptions": {
            "Mild": "🟢 Mild / Feeling Good (Mild / Normal)",
            "Moderate": "🟡 Moderate / Need Rest (Moderate / Need Rest)",
            "Severe": "🔴 Severe / Feeling Unwell (Severe / Bad)"
        },
        "symptomsDict": {
            "Fever": "🌡️ Fever",
            "Headache": "🤕 Headache",
            "Cough": "🤧 Cough / Cold",
            "Vomiting": "🤮 Vomiting",
            "Stomach Pain": "🤢 Stomach Ache",
            "Chest Discomfort": "💔 Chest Tightness",
            "Diarrhea": "💧 Diarrhea",
            "Body Ache": "😫 Body Pain",
            "Dizziness": "😵 Dizziness"
        },
        "painBadges": {
            0: "0 - No Pain 😊",
            "mild": "Mild Pain 😐",
            "mod": "Moderate Pain 😣",
            "high": "High / Severe Pain 😫",
            "worst": "10 - Extreme Worst Pain 🚨"
        },
        "saveLogBtn": "💾 Save Daily Health Check-in",
        "chartsTitle": "📈 Monthly Vitals Progression Charts",
        "chartSwitches": {
            "bp": "Blood Pressure",
            "sugar-temp": "Sugar & Temp",
            "pulse-spo2": "Pulse & SpO2"
        },
        "chartLegends": {
            "sysBp": "Systolic BP (mmHg)",
            "diaBp": "Diastolic BP (mmHg)",
            "sugar": "Blood Sugar (mg/dL)",
            "temp": "Temperature (°F)",
            "pulse": "Heart Rate / Pulse (BPM)",
            "spo2": "Oxygen SpO2 (%)"
        },
        "timelineTitle": "📋 Daily Check-in History",
        "analyzeChartBtn": "🤖 AI Review My Vitals Log",
        "deleteEntryText": "🗑️ Delete Entry",

        # View 5: Doctor Report
        "reportTitle": "Monthly Clinical Health Summary for Doctor",
        "reportDesc": "Generate a professional, structured clinical report from your daily health check-ins. Send it to your real doctor via Email, WhatsApp, or Print/Save as PDF.",
        "lblPatName": "Patient Name:",
        "lblPatAge": "Age & Gender:",
        "lblDocEmail": "Doctor's Email (for Sending):",
        "lblDocPhone": "Doctor's WhatsApp / Mobile:",
        "phPatName": "e.g. Ramesh Kumar",
        "phPatAge": "e.g. 48 Y / Male",
        "phDocPhone": "e.g. 919876543210",
        "generateReportBtn": "✨ Generate Monthly Doctor Report",
        "reportEmptyText": "Click 'Generate Monthly Doctor Report' above to compile your recorded daily logs into a hospital-grade physician handover summary.",
        "docTitle": "HealthMate AI • Monthly Tele-Health Vitals Summary",
        "docSubtitle": "Primary Health Center (PHC) & Remote Community Clinical Handover Sheet",
        "docBadge": "CONFIDENTIAL MEDICAL REPORT",
        "docLblName": "Patient Name:",
        "docLblDemo": "Demographics:",
        "docLblLoc": "Location Context:",
        "docLocVal": "Remote / Hospital > 30 km",
        "docLblWin": "Monitoring Window:",
        "docWinVal": "Past 30 Days (Daily Logs)",
        "docSec1Title": "1. Vitals Overview & Monthly Statistics",
        "docSec2Title": "2. Clinical Red Flags & Threshold Deviations",
        "docSec3Title": "3. Symptom Frequency Distribution",
        "docSec4Title": "4. Physician Handover Memo & Clinical Observations",
        "docSec5Title": "5. Attending Doctor's Prescription & Clinical Notes (For Doctor Use)",
        "docRxLine": "Rx / Medications Prescribed: ___________________________________________________________",
        "docLabLine": "Clinical Investigation Advised: [ ] Blood Routine [ ] HbA1c [ ] ECG [ ] Chest X-Ray [ ] Other: ______",
        "docDateLine": "Date: _______________",
        "docSignLine": "Doctor's Signature & Reg. No: ___________________________",
        "docDisclaimer": "⚠️ Clinical Notice: This summary was aggregated from patient-recorded daily home vitals via HealthMate AI. It is intended to assist medical practitioners during clinical reviews or tele-consultations.",
        "emailDoctorBtn": "✉️ Email to Doctor",
        "whatsappDoctorBtn": "💬 Send via WhatsApp",
        "printReportBtn": "🖨️ Print / Save as PDF",

        # Stat Card Labels
        "statAvgBp": "Average BP (mmHg)",
        "statPeakBp": "Peak BP Reading",
        "statAvgSugar": "Avg Glucose (mg/dL)",
        "statPeakSugar": "Peak Glucose (mg/dL)",
        "statAvgSpo2": "Avg SpO2",
        "statLowest": "Lowest",
        "statAvgPulse": "Avg Pulse Rate (BPM)",
        "statAvgTemp": "Avg Body Temp",
        "statDaysMonitored": "Days Monitored",

        # Footer
        "disclaimerHeader": "Important Medical Disclaimer",
        "disclaimerBody": "HealthMate AI is an informational and remote emergency assistance tool built for communities with distant medical facilities. It is not a qualified doctor, cannot deliver confirmed clinical diagnoses, and does not prescribe prescription-only medicines. Always consult an authorized medical practitioner. In acute emergencies, call 108 or proceed immediately to the nearest hospital.",
        "hackathonFooter": "AWS User Group Madurai Strands SDK Hackathon • Remote Healthcare Track • © 2026",

        "suggestions": [
            "Severe cut bleeding won't stop, what should I do right now?",
            "What essential medicines should I buy to stock at home in a remote village?",
            "First aid steps if a stray dog bites someone in an isolated area",
            "My BP was 148/94 and sugar 185 today, is this dangerous?",
            "How to prepare WHO-ORS solution properly for dehydration"
        ]
    },

    "Tamil": {
        # Navigation Tabs
        "tabChat": "💬 அரட்டை",
        "tabWounds": "🩹 அவசர முதலுதவி",
        "tabMeds": "🛒 மருந்து பட்டியல்",
        "tabChart": "📊 தினசரி பதிவு & வரைபடம்",
        "tabReport": "📄 மருத்துவர் அறிக்கை",

        # Header & Banners
        "brandTagline": "தொலைதூர அவசர முதலுதவி & தமிழ் AI உடல்நல உதவியாளர்",
        "statusReady": "AI தயார்",
        "statusConnecting": "இணைகிறது...",
        "networkOnline": "இணையத்தில் உள்ளது",
        "networkOffline": "ஆஃப்லைன் பயன்முறை",
        "cacheReady": "ஆஃப்லைன் பேக்: தயார்",
        "clearBtnTitle": "அரட்டை வரலாற்றை அழிக்க",
        "dailyBannerTitle": "தினசரி உடல்நல பரிசோதனை: இன்று உங்கள் உடல்நிலை எப்படி உள்ளது?",
        "dailyBannerDesc": "மருத்துவமனை வெகு தொலைவில் உள்ளதா? உங்கள் இரத்த அழுத்தம், சர்க்கரை மற்றும் அறிகுறிகளை தினமும் குறித்து வையுங்கள்.",
        "quickCheckinBtn": "➕ இன்றைய அளவை பதிவு செய்ய",
        "emergencyTitle": "அவசர மருத்துவ எச்சரிக்கை",
        "emergencyDesc": "கடுமையான மார்பு வலி, மூச்சுத் திணறல், தீவிர இரத்தப்போக்கு அல்லது மயக்கம் ஏற்பட்டால் உடனடியாக 108 அழைக்கவும் அல்லது ஆரம்ப சுகாதார நிலையத்திற்கு (PHC) செல்லவும்.",
        "emergencyBtn": "108 அழைக்க 📞",

        # Offline Banner & Triage
        "offlineBannerTitle": "ஆஃப்லைன் பயன்முறை • இணைய இணைப்பு இல்லை",
        "offlineBannerDesc": "தற்போது இணைய இணைப்பு துண்டிக்கப்பட்டுள்ளது. நேரலை AI ஆலோசனை பெற முடியாது, ஆனால் உங்களுக்கான முழுமையான ஆஃப்லைன் அவசர முதலுதவி வழிகாட்டி மற்றும் பதிவுகள் தயாராக உள்ளன.",
        "offlineBtnText": "🩹 அவசர முதலுதவி வழிகாட்டியைத் திறக்க",
        "offlineGuideStatus": "ஆஃப்லைன் முதலுதவி பேக்: உலாவியின் Cache Storage-ல் பதிவிறக்கம் செய்யப்பட்டு தயாராக உள்ளது",
        "triageTitle": "முக்கிய அவசர அறிவிப்பு: எப்போது உடனடியாக 108 அழைக்க வேண்டும் / மருத்துவமனைக்கு செல்ல வேண்டும்",
        "triageSubtitle": "முதலுதவி என்பது மருத்துவமனை செல்லும் வரை உயிரைக் காப்பாற்ற மட்டுமே. இது மருத்துவரின் தீவிர சிகிச்சை அல்லது அறுவை சிகிச்சைக்கு மாற்றாகாது.",
        "triageRushTitle": "🚑 உடனடியாக 108 அழைக்க வேண்டிய அவசர நிலைகள்:",
        "triageRoleTitle": "🛡️ இந்த ஆஃப்லைன் வழிகாட்டியை எவ்வாறு பயன்படுத்த வேண்டும்:",
        "triageRoleDesc": "தொலைதூர கிராமத்திலோ அல்லது நெட்வொர்க் இல்லாத இடத்திலோ இருக்கும் போது: கீழே உள்ள காய வகையைத் தேர்ந்தெடுக்கவும். 4 படிநிலைகளை பின்பற்றி ஆபத்துகளைத் தவிர்த்து ஆரம்ப சுகாதார நிலையத்திற்கு நோயாளியை அழைத்துச் செல்லவும்.",
        "triageRushList": [
            "அழுத்திப் பிடித்தும் நிற்காத தீவிர இரத்தப்போக்கு அல்லது இரத்தம் பீறிடுதல்",
            "பாதிக்கப்பட்டவர் சுயநினைவின்றி இருத்தல் அல்லது சுவாசம் நின்று போதல் (உடனே CPR தொடங்கவும்)",
            "விஷப் பாம்பு கடி (1-2 மணி நேரத்திற்குள் மருத்துவமனையில் ASV மருந்து பெற வேண்டும்)",
            "உள்ளங்கையை விட பெரிய தீக்காயங்கள் அல்லது முகம், மூட்டுகளில் ஏற்பட்ட தீக்காயங்கள்",
            "கழுத்து, முதுகுத்தண்டு அல்லது தொடை எலும்பு முறிவு சந்தேகம் (நோயாளியை அசைக்கக் கூடாது)",
            "நாய் அல்லது வெறி விலங்கு கடித்தல் (24 மணி நேரத்திற்குள் ரேபிஸ் தடுப்பூசி பெற வேண்டும்)"
        ],

        # View 1: Chat
        "hackathonTag": "தொலைதூர மருத்துவ AI • Strands SDK & Gemini",
        "heroTitle": "உங்கள் உடல்நலம், உங்கள் தாய்மொழியில்.",
        "heroSubtitle": "காய சிகிச்சை, வீட்டிலேயே இருப்பு வைக்க வேண்டிய அத்தியாவசிய மருந்துகள், மற்றும் தினசரி இரத்த அழுத்த பதிவுகள்.",
        "suggestLabel": "💡 மாதிரி கேள்விகள்:",
        "chatTitle": "உடல்நல ஆலோசனை அரட்டை",
        "chatSubtitle": "தகவல் வழிகாட்டுதல் மட்டுமே • மருத்துவ உறுதிப்படுத்தல் அல்ல",
        "voiceLabel": "குரல் வழி உள்ளீடு",
        "voiceListening": "கேட்கிறது...",
        "welcomeHtml": "<strong>வணக்கம்! நான் HealthMate AI. 👋</strong><br><br>தொலைதூர பகுதிகளில் உள்ளவர்களுக்கான உங்கள் மருத்துவ வழிகாட்டி நான். <strong>அவசர காய சிகிச்சை</strong>, வீட்டில் வைக்க வேண்டிய <strong>அத்தியாவசிய முதலுதவி மருந்துகள்</strong>, தினசரி <strong>இரத்த அழுத்தம்/சர்க்கரை கண்காணிப்பு</strong> மற்றும் உங்கள் <strong>மருத்துவருக்கான மாதாந்திர அறிக்கை</strong> தயார் செய்ய நான் உதவுவேன்.<br><br><em>இன்று உங்களுக்கு நான் எவ்வாறு உதவ வேண்டும்?</em>",
        "chatPlaceholder": "அறிகுறிகள், காயங்கள் பற்றி தமிழில் எழுதுங்கள் (எ.கா: 3 நாட்களாக காய்ச்சல், வெட்டுக்காயம்)...",
        "sendText": "அனுப்பு",
        "privacyNote": "🔒 பாதுகாப்பானது: தொலைதூர கிராமங்களுக்கான பாதுகாப்பான மருத்துவ வழிகாட்டி.",
        "chatOfflineWarning": "⚠️ **ஆஃப்லைன் பயன்முறை: இணைய இணைப்பு இல்லாமல் AI ஆலோசனை பெற முடியாது.**<br><br>தற்போது இணைய இணைப்பு துண்டிக்கப்பட்டுள்ளது. நேரலை AI ஆலோசனை பெற முடியாது, ஆனால் உங்களுக்கான **முழுமையான ஆஃப்லைன் அவசர முதலுதவி வழிகாட்டி** உங்கள் உலாவியில் தயாராக சேமிக்கப்பட்டுள்ளது.<br><br>👉 உடனடி முதலுதவி படிகளைப் பார்க்க மேலே உள்ள <strong>[🩹 அவசர முதலுதவி]</strong> பகுதியைத் தேர்ந்தெடுக்கவும் (வெட்டுக்காயம், இரத்தப்போக்கு, தீக்காயம், பாம்பு கடி, நாய் கடி, மயக்கம்/CPR).<br><br><em>உயிருக்கு ஆபத்தான அவசர நிலையில் உடனடியாக <strong>108</strong> அழைக்கவும்.</em>",

        # View 2: Offline First-Aid Tutorial
        "woundsTitle": "முழுமையான ஆஃப்லைன் அவசர முதலுதவி வழிகாட்டி",
        "woundsDesc": "மருத்துவமனை அல்லது ஆம்புலன்ஸ் வர இயலாத தொலைதூர கிராமங்களுக்கான படி-படியான மருத்துவ முதலுதவி வழிகாட்டி. ஆஃப்லைனில் முழுமையாக இயங்கும்.",
        "woundsSelectLabel": "முதலுதவி அல்லது அவசர பாதிப்பு வகையைத் தேர்ந்தெடுக்கவும்:",
        "woundPills": {
            "severe-bleeding": "🚨 தீவிர இரத்தப்போக்கு & டூர்னிகெட்",
            "minor-cuts": "🩹 சிறிய வெட்டுக்காயம் & சிராய்ப்பு",
            "burns": "🔥 தீக்காயங்கள் (1st முதல் 3rd Degree)",
            "fractures": "🦴 எலும்பு முறிவு & அவசர ஸ்பிளின்ட்",
            "snakebites": "🐍 பாம்பு கடி (ASV விஷ முறிவு நெறிமுறை)",
            "animal-bites": "🐕 நாய் கடி (ரேபிஸ் தடுப்பூசி)",
            "unconsciousness": "🫀 மயக்கம் & CPR (சுயநினைவின்மை)",
            "puncture-wounds": "🔩 ஆணி / முள் குத்திய காயம் (டெட்டனஸ்)",
            "sepsis": "⚠️ சீழ் தொற்று & செப்சிஸ் ஆபத்து"
        },

        # View 3: Medicine Kit
        "medsTitle": "வீட்டில் இருப்பு வைக்க வேண்டிய அத்தியாவசிய மருந்துகள் பட்டியல்",
        "medsDesc": "மருந்தகங்கள் குறைவாக உள்ள ஊர்களில் ஒவ்வொரு வீட்டிலும் வாங்கி வைக்க வேண்டிய பாதுகாப்பான OTC முதலுதவி மருந்துகள்.",
        "medFilters": {
            "all": "அனைத்து பொருட்கள்",
            "wound": "🩹 காயம் & கிருமிநாசினி",
            "fever": "🌡️ காய்ச்சல் & வலி",
            "stomach": "🤢 வயிறு & ORS",
            "allergy": "🐝 ஒவ்வாமை & தீக்காயம்",
            "tools": "🩺 மருத்துவக் கருவிகள்"
        },
        "copyMedsBtn": "📋 மருந்து பட்டியலை நகலெடு",
        "printMedsBtn": "🖨️ பட்டியலை அச்சிடு",

        # View 4: Daily Log & Chart
        "chartSectionTitle": "தினசரி உடல்நலப் பதிவு & வரைபட கண்காணிப்பு",
        "chartSectionDesc": "தினசரி இரத்த அழுத்தம், சர்க்கரை அளவு, ஆக்ஸிஜன் மற்றும் காய்ச்சலை பதிவு செய்யுங்கள். வரைபடம் மூலம் நோய்களை முன்கூட்டியே கண்டறியலாம்.",
        "logFormTitle": "☀️ இன்றைய உடல்நலப் பதிவு",
        "lblDate": "தேதி (வருடம்-மாதம்-நாள்):",
        "lblTime": "அளவிடப்பட்ட நேரம்:",
        "lblSysBp": "சிஸ்டாலிக் BP (உயர் இரத்த அழுத்தம் / mmHg):",
        "lblDiaBp": "டயஸ்டாலிக் BP (குறைந்த இரத்த அழுத்தம் / mmHg):",
        "lblSugar": "இரத்த சர்க்கரை அளவு (mg/dL):",
        "lblPulse": "நாடித் துடிப்பு / இதயத் துடிப்பு (BPM):",
        "lblSpo2": "இரத்த ஆக்சிஜன் அளவு - SpO2 (%):",
        "lblTemp": "உடல் வெப்பநிலை (°F):",
        "lblPain": "வலி தீவிரம் (0 = வலி இல்லை, 10 = தாங்க முடியாத வலி):",
        "lblSymptomsSelect": "இன்று ஏற்பட்ட அறிகுறிகளைத் தேர்ந்தெடுக்கவும்:",
        "lblSeverity": "இன்றைய பொதுவான உடல்நிலை:",
        "lblNotes": "கூடுதல் குறிப்புகள் / உட்கொண்ட மருந்துகள்:",
        "phSysBp": "எ.கா: 120",
        "phDiaBp": "எ.கா: 80",
        "phSugar": "எ.கா: 95 அல்லது 140",
        "phPulse": "எ.கா: 72",
        "phSpo2": "எ.கா: 98",
        "phTemp": "எ.கா: 98.6",
        "phNotes": "எ.கா: பாராசிட்டமால் சாப்பிட்டேன், ஓய்வெடுத்தேன், ORS குடித்தேன்...",
        "severityOptions": {
            "Mild": "🟢 லேசானது / நலம் (Mild / Normal)",
            "Moderate": "🟡 மிதமானது / ஓய்வு தேவை (Moderate / Need Rest)",
            "Severe": "🔴 தீவிரமானது / உடல்நிலை மோசம் (Severe / Bad)"
        },
        "symptomsDict": {
            "Fever": "🌡️ காய்ச்சல்",
            "Headache": "🤕 தலைவலி",
            "Cough": "🤧 சளி / இருமல்",
            "Vomiting": "🤮 வாந்தி",
            "Stomach Pain": "🤢 வயிற்று வலி",
            "Chest Discomfort": "💔 நெஞ்சு அழுத்தம் / வலி",
            "Diarrhea": "💧 வயிற்றுப்போக்கு / பேதி",
            "Body Ache": "😫 உடல் வலி / சோர்வு",
            "Dizziness": "😵 தலைசுற்றல்"
        },
        "painBadges": {
            0: "0 - வலி இல்லை 😊",
            "mild": "லேசான வலி 😐",
            "mod": "மிதமான வலி 😣",
            "high": "கடுமையான தீவிர வலி 😫",
            "worst": "10 - தாங்க முடியாத உச்சகட்ட வலி 🚨"
        },
        "saveLogBtn": "💾 இன்றைய பதிவை சேமிக்க",
        "chartsTitle": "📈 மாதாந்திர உடல்நல அளவீட்டு வரைபடம்",
        "chartSwitches": {
            "bp": "இரத்த அழுத்தம் (BP)",
            "sugar-temp": "சர்க்கரை & வெப்பநிலை",
            "pulse-spo2": "நாடி & ஆக்சிஜன்"
        },
        "chartLegends": {
            "sysBp": "சிஸ்டாலிக் BP (mmHg)",
            "diaBp": "டயஸ்டாலிக் BP (mmHg)",
            "sugar": "இரத்த சர்க்கரை (mg/dL)",
            "temp": "உடல் வெப்பநிலை (°F)",
            "pulse": "நாடித் துடிப்பு (BPM)",
            "spo2": "ஆக்சிஜன் SpO2 (%)"
        },
        "timelineTitle": "📋 பதிவு செய்யப்பட்ட தினசரி வரலாறு",
        "analyzeChartBtn": "🤖 AI மூலம் எனது பதிவுகளை ஆராய்க",
        "deleteEntryText": "🗑️ பதிவை நீக்கு",

        # View 5: Doctor Report
        "reportTitle": "மருத்துவரிடம் காட்டுவதற்கான மாதாந்திர உடல்நல அறிக்கை",
        "reportDesc": "உங்கள் தினசரி பதிவுகளை மருத்துவமனை அளவிலான அறிக்கையாக மாற்றி, உங்கள் மருத்துவருக்கு Email, WhatsApp அல்லது Print மூலம் எளிதாக அனுப்பலாம்.",
        "lblPatName": "நோயாளி பெயர்:",
        "lblPatAge": "வயது மற்றும் பாலினம்:",
        "lblDocEmail": "மருத்துவரின் மின்னஞ்சல் (Email):",
        "lblDocPhone": "மருத்துவரின் வாட்ஸ்அப் / கைபேசி எண்:",
        "phPatName": "எ.கா: ரமேஷ் குமார் / செல்வி",
        "phPatAge": "எ.கா: 48 வயது / ஆண்",
        "phDocPhone": "எ.கா: 919876543210",
        "generateReportBtn": "✨ மாதாந்திர மருத்துவ அறிக்கையை உருவாக்குக",
        "reportEmptyText": "மேலே உள்ள 'மாதாந்திர மருத்துவ அறிக்கையை உருவாக்குக' பொத்தானை அழுத்தி, உங்கள் மருத்துவருக்கான விரிவான அறிக்கையை தயார் செய்யுங்கள்.",
        "docTitle": "HealthMate AI • மாதாந்திர தொலைதூர மருத்துவ அறிக்கை",
        "docSubtitle": "ஆரம்ப சுகாதார நிலையம் (PHC) மற்றும் குடும்ப மருத்துவ குறிப்பேடு",
        "docBadge": "இரகசிய மருத்துவ ஆவணம்",
        "docLblName": "நோயாளி பெயர்:",
        "docLblDemo": "விவரம்:",
        "docLblLoc": "வசிப்பிடம்:",
        "docLocVal": "தொலைதூர கிராமம் (மருத்துவமனை > 30 கி.மீ)",
        "docLblWin": "கண்காணிப்பு காலம்:",
        "docWinVal": "கடந்த 30 நாட்கள் (தினசரி அளவீடுகள்)",
        "docSec1Title": "1. மாதாந்திர உடல்நல புள்ளிவிவரங்கள் & சராசரிகள்",
        "docSec2Title": "2. மருத்துவ எச்சரிக்கைகள் & வரம்பு மீறல்கள்",
        "docSec3Title": "3. அறிகுறிகள் தோன்றிய நாட்களின் எண்ணிக்கை",
        "docSec4Title": "4. மருத்துவருக்கான AI பகுப்பாய்வு குறிப்பு",
        "docSec5Title": "5. மருத்துவரின் மருந்து பரிந்துரை & குறிப்புகள் (மருத்துவர் பயன்பாட்டிற்கு)",
        "docRxLine": "பரிந்துரைக்கப்பட்ட மருந்துகள் (Rx): ___________________________________________________________",
        "docLabLine": "பரிந்துரைக்கப்பட்ட சோதனைகள்: [ ] இரத்தப் பரிசோதனை [ ] HbA1c [ ] ECG [ ] மார்பு எக்ஸ்ரே [ ] பிற: ______",
        "docDateLine": "தேதி: _______________",
        "docSignLine": "மருத்துவரின் கையொப்பம் & பதிவு எண்: ___________________________",
        "docDisclaimer": "⚠️ மருத்துவ குறிப்பு: இந்த அறிக்கை நோயாளியால் பதிவு செய்யப்பட்ட தினசரி வீட்டு அளவீடுகளின் அடிப்படையில் தொகுக்கப்பட்டது. மருத்துவர் அல்லது ஆரம்ப சுகாதார நிலைய மருத்துவ அலுவலரின் ஆலோசனைக்கு மட்டுமே.",
        "emailDoctorBtn": "✉️ மருத்துவருக்கு மின்னஞ்சல் அனுப்பு",
        "whatsappDoctorBtn": "💬 வாட்ஸ்அப் மூலம் அனுப்பு",
        "printReportBtn": "🖨️ அச்சிடு / PDF சேமி",

        # Stat Card Labels
        "statAvgBp": "சராசரி BP (mmHg)",
        "statPeakBp": "அதிகபட்ச BP அளவு",
        "statAvgSugar": "சராசரி சர்க்கரை (mg/dL)",
        "statPeakSugar": "அதிகபட்ச சர்க்கரை (mg/dL)",
        "statAvgSpo2": "சராசரி ஆக்சிஜன்",
        "statLowest": "குறைந்தது",
        "statAvgPulse": "சராசரி நாடித் துடிப்பு (BPM)",
        "statAvgTemp": "சராசரி வெப்பநிலை",
        "statDaysMonitored": "கண்காணிக்கப்பட்ட நாட்கள்",

        # Footer
        "disclaimerHeader": "முக்கிய மருத்துவ மறுப்புரை",
        "disclaimerBody": "HealthMate AI என்பது தொலைதூர கிராமங்களுக்கான முதலுதவி மற்றும் பொது உடல்நல தகவல் வழிகாட்டி மட்டுமே. இது மருத்துவர் அல்ல, நோய்களைக் கண்டறியவோ மருந்துச் சீட்டு தரவோ முடியாது. தீவிர உடல்நலப் பிரச்சனைகளுக்கு உடனடியாக மருத்துவரை அணுகவும் அல்லது அவசர உதவிக்கு 108 அழைக்கவும்.",
        "hackathonFooter": "AWS User Group Madurai Strands SDK Hackathon • தொலைதூர மருத்துவ சேவை • © 2026",

        "suggestions": [
            "ஆழமான வெட்டுக்காயத்தில் இரத்தம் நிற்கவில்லை, உடனே என்ன செய்ய வேண்டும்?",
            "கிராமத்தில் உள்ள வீட்டில் வாங்கி வைக்க வேண்டிய முதலுதவி மருந்துகள் என்ன?",
            "தெரு நாய் கடித்தால் உடனடியாக செய்ய வேண்டிய முதலுதவி படிகள் என்ன?",
            "இன்று எனது BP 148/94 மற்றும் சர்க்கரை 185 உள்ளது, இது ஆபத்தானதா?",
            "நீரிழப்புக்கு ORS கரைசலை சரியான முறையில் தயாரிப்பது எப்படி?"
        ]
    }
}

def get_translations(lang: str = "English") -> dict:
    normalized = "Tamil" if lang in ("Tamil", "ta") else "English"
    return TRANSLATIONS.get(normalized, TRANSLATIONS["English"])
