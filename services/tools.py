"""
Health tools for the Bilingual AI Health Assistant.
Each function decorated with @tool is registered with the Strands Agent.
"""

from strands import tool


EMERGENCY_KEYWORDS_EN = [
    "chest pain", "chest pressure", "heart attack", "can't breathe",
    "cannot breathe", "difficulty breathing", "shortness of breath",
    "stroke", "face drooping", "arm weakness", "speech difficulty",
    "unconscious", "unresponsive", "not breathing", "stopped breathing",
    "severe bleeding", "heavy bleeding", "won't stop bleeding",
    "overdose", "poisoning", "swallowed poison", "allergic reaction",
    "anaphylaxis", "throat closing", "swelling throat",
    "seizure", "convulsion", "fits", "collapsed",
    "head injury", "diabetic coma", "blood sugar very low",
    "suicidal", "want to die", "kill myself",
    "choking", "can't swallow", "airway blocked",
]

EMERGENCY_KEYWORDS_TA = [
    "மார்பு வலி", "இதய வலி", "மாரடைப்பு", "சுவாசிக்க முடியவில்லை",
    "மூச்சு திணறல்", "மூச்சு சிரமம்", "பக்கவாதம்", "முகம் கோணல்",
    "கை தளர்வு", "பேச்சு தடை", "நினைவிழந்தார்", "நினைவற்று",
    "தீவிர இரத்தப்போக்கு", "அதிக இரத்தம்", "அதிகப்படியான மருந்து",
    "விஷம் குடித்தார்", "ஒவ்வாமை", "தொண்டை வீக்கம்",
    "வலிப்பு", "கைகால் வலிப்பு", "மயக்கம்", "விழுந்து விட்டார்",
    "தலை காயம்", "நீரிழிவு கோமா", "தற்கொலை", "மூச்சு அடைப்பு",
]


def is_emergency(text: str) -> bool:
    text_lower = text.lower()
    for kw in EMERGENCY_KEYWORDS_EN:
        if kw in text_lower:
            return True
    for kw in EMERGENCY_KEYWORDS_TA:
        if kw in text_lower:
            return True
    return False


@tool
def check_for_emergency(symptoms_description: str, language: str = "English") -> str:
    """
    Check if the described symptoms are a medical emergency.
    Call this tool FIRST whenever a user describes acute symptoms.
    """
    if not is_emergency(symptoms_description):
        return ""
    if language == "Tamil":
        return (
            "EMERGENCY_DETECTED\n"
            "AMBULANCE_NUMBER: 108\n\n"
            "🚨 அவசர எச்சரிக்கை!\n\n"
            "நீங்கள் விவரித்த அறிகுறிகள் உடனடி அவசர மருத்துவ சிகிச்சை தேவைப்படலாம்.\n\n"
            "உடனடியாக செய்ய வேண்டியவை:\n"
            "• தாமதிக்காமல் 108 (அவசர உதவி) அல்லது அருகிலுள்ள மருத்துவமனையை அழையுங்கள்.\n"
            "• நோயாளியை தனியாக விடாதீர்கள்.\n"
            "• நோயாளியை அமைதியாகவும் சாய்வாகவும் படுக்க வைக்கவும்.\n"
            "• இது உயிருக்கு ஆபத்தான நிலையாக இருக்கலாம். AI-ஐ நம்பி நேரத்தை வீணடிக்காதீர்கள்!"
        )
    else:
        return (
            "EMERGENCY_DETECTED\n"
            "AMBULANCE_NUMBER: 108\n\n"
            "🚨 EMERGENCY ALERT!\n\n"
            "The symptoms described may represent an acute medical emergency.\n\n"
            "Immediate Actions Required:\n"
            "• Call 108 (or your local emergency number) immediately.\n"
            "• Do not leave the person alone.\n"
            "• Keep the individual seated or lying down comfortably.\n"
            "• Do not delay critical medical transport. Seek emergency care NOW!"
        )


@tool
def assess_symptom_status(symptom: str, duration_days: int = 1, severity: str = "moderate", language: str = "English") -> str:
    """
    Assess whether a symptom's duration and severity is considered mild (manageable at home),
    moderate (needs close monitoring), or bad/urgent (requires doctor visit).
    Also provides 2-3 specific follow-up questions to ask the user.
    """
    s = symptom.lower()
    is_fever = any(w in s for w in ["fever", "காய்ச்சல்", "temp"])
    is_headache = any(w in s for w in ["headache", "தலைவலி"])
    is_stomach = any(w in s for w in ["stomach", "வயிறு", "abdominal", "loose"])

    if language == "Tamil":
        if is_fever:
            if duration_days >= 3:
                status = "🔴 தீவிர கவனிப்பு தேவை (Bad / Concerning)"
                analysis = f"{duration_days} நாட்களுக்கும் மேலாக காய்ச்சல் நீடிப்பது சாதாரண வைரஸ் காய்ச்சலை விட டெங்கு, டைபாய்டு அல்லது பாக்டீரியா தொற்றாக இருக்க வாய்ப்புள்ளது. வீட்டு சிகிச்சையுடன் நிறுத்தாமல் மருத்துவ பரிசோதனை செய்வது அவசியம்."
            else:
                status = "🟡 மிதமான நிலை (Moderate - கண்காணிக்கவும்)"
                analysis = f"{duration_days} நாள் காய்ச்சல் பொதுவான வைரஸ் தொற்றாக இருக்கலாம். போதுமான ஓய்வும் நீராகாரமும் தேவை."
            questions = [
                "1. உடல் வெப்பநிலை எத்தனை டிகிரி உள்ளது? (எ.கா: 100°F அல்லது 102°F?)",
                "2. குளிர் நடுக்கம், வாந்தி, அல்லது உடலில் ஏதேனும் சிவந்த தடிப்புகள் உள்ளதா?",
                "3. சிறுநீர் வழக்கமான அளவில் வெளியேறுகிறதா அல்லது அடர் மஞ்சளாக உள்ளதா?"
            ]
        elif is_headache:
            if duration_days >= 4:
                status = "🔴 மருத்துவ ஆலோசனை தேவை (Needs Doctor Visit)"
                analysis = f"{duration_days} நாட்களாக தொடர்ந்து தலைவலி இருப்பது இரத்த அழுத்தம், சைனஸ் அல்லது கண் பார்வைக் கோளாறுகளால் இருக்கலாம்."
            else:
                status = "🟢 ஆரம்ப நிலை (Mild / Manageable)"
                analysis = "நீரிழப்பு, தூக்கமின்மை அல்லது மன அழுத்தத்தால் ஏற்பட்டிருக்கலாம்."
            questions = [
                "1. தலைவலி எந்த பகுதியில் உள்ளது (முழு தலை, நெற்றி அல்லது ஒரு பக்கம் மட்டும்)?",
                "2. பார்வை மங்குதல், குமட்டல் அல்லது வெளிச்சத்தைப் பார்த்தால் கூச்சம் உள்ளதா?",
                "3. போதுமான அளவு தண்ணீர் குடித்தீர்களா மற்றும் தூங்கினீர்களா?"
            ]
        else:
            status = "🟡 கண்காணிக்க வேண்டிய நிலை (Needs Monitoring)"
            analysis = f"{duration_days} நாட்களாக இந்த அறிகுறி உள்ளது. தீவிரமடைந்தால் மருத்துவரை அணுகவும்."
            questions = [
                "1. இந்த வலி அல்லது அசௌகரியம் எந்த நேரத்தில் அதிகமாக உள்ளது?",
                "2. இதற்கு முன் இதே போன்ற பிரச்சனை ஏற்பட்டுள்ளதா?",
                "3. வேறு ஏதேனும் புதிய அறிகுறிகள் தென்படுகின்றனவா?"
            ]

        return (
            f"📊 நிலை மதிப்பீடு (Health Status): {status}\n\n"
            f"விளக்கம்:\n{analysis}\n\n"
            f"❓ தெளிவான வழிகாட்டலுக்கு இந்த 3 கேள்விகளுக்கு பதிலளியுங்கள்:\n" +
            "\n".join(questions)
        )
    else:
        if is_fever:
            if duration_days >= 3:
                status = "🔴 Concerning / Requires Doctor Evaluation (Bad Sign)"
                analysis = f"A fever lasting {duration_days} days or more warrants clinical attention. Persistent fevers can indicate conditions such as dengue, typhoid, urinary tract infection, or bacterial illness that require blood tests."
            else:
                status = "🟡 Moderate (Monitor Closely at Home)"
                analysis = f"A fever for {duration_days} days is commonly viral. Rest and proper hydration are critical during this phase."
            questions = [
                "1. What is your current temperature reading (e.g., 100°F or above 102°F)?",
                "2. Do you have severe chills, body rashes, vomiting, or breathing difficulty?",
                "3. Are you able to keep fluids down and urinating normally?"
            ]
        elif is_headache:
            if duration_days >= 4:
                status = "🔴 Needs Medical Assessment (Persistent)"
                analysis = f"A headache lasting {duration_days} days without relief should be evaluated by a physician for blood pressure, sinusitis, or migraine."
            else:
                status = "🟢 Mild to Moderate (Commonly Manageable)"
                analysis = "Often triggered by dehydration, eye strain, lack of sleep, or tension."
            questions = [
                "1. Is the pain throbbing on one side, or a steady band around the forehead?",
                "2. Are you experiencing nausea, vomiting, or sensitivity to light/sound?",
                "3. Have you checked your blood pressure recently?"
            ]
        else:
            status = "🟡 Moderate Condition (Observe Closely)"
            analysis = f"The symptom has persisted for {duration_days} days. If pain worsens or does not improve within 48 hours, consult a physician."
            questions = [
                "1. On a scale of 1 to 10, how severe is the discomfort right now?",
                "2. Does anything make it better or worse (e.g., eating, resting, walking)?",
                "3. Have you started any new foods or medications recently?"
            ]

        return (
            f"📊 Condition Status: {status}\n\n"
            f"Clinical Context:\n{analysis}\n\n"
            f"❓ To help you better, please answer these quick follow-up questions:\n" +
            "\n".join(questions)
        )


@tool
def get_otc_medication_info(condition: str, language: str = "English") -> str:
    """
    Provide supportive over-the-counter (OTC) medication options and essential precautions.
    Clearly notes that this is informational and not an individualized doctor prescription.
    """
    c = condition.lower()
    if language == "Tamil":
        disclaimer = "\n\n⚠️ மருத்துவ எச்சரிக்கை: இது பொதுவான OTC மருந்துத் தகவல் மட்டுமே. தனிப்பட்ட மருந்துச் சீட்டு அல்ல. மருத்துவர் அல்லது மருந்தாளுநரின் (Pharmacist) ஆலோசனை பெற்று உட்கொள்ளவும்."
        if any(w in c for w in ["fever", "காய்ச்சல்", "body pain", "உடல் வலி"]):
            return (
                "💊 காய்ச்சல் & உடல் வலிக்கான பொதுவான முதலுதவி மருந்துகள்:\n\n"
                "1. Paracetamol (பாராசிட்டமால் - எ.கா: Dolo 650 / Calpol):\n"
                "• பெரியவர்களுக்கு: 500mg முதல் 650mg வரை, தேவைப்பட்டால் 6-8 மணி நேர இடைவெளியில்.\n"
                "• ஒரு நாளில் 4 மாத்திரைகளுக்கு (3000mg) மேல் உட்கொள்ளக் கூடாது (கல்லீரல் பாதுகாப்பு).\n"
                "• வெறும் வயிற்றில் உட்கொள்வதைத் தவிர்க்கவும்.\n\n"
                "2. ORS (Oral Rehydration Solution) / எலக்ட்ரோலைட்:\n"
                "• காய்ச்சலின் போது ஏற்படும் வியர்வை மற்றும் நீரிழப்பைத் தடுக்க ORS அல்லது இளநீர் அருந்தவும்.\n\n"
                "❌ செய்யக்கூடாதவை:\n"
                "• மருத்துவர் பரிந்துரை இன்றி ஆன்டிபயாடிக் (Antibiotics) மருந்துகளைத் தாங்களாகவே வாங்கக் கூடாது."
            ) + disclaimer
        elif any(w in c for w in ["stomach", "acidity", "gastric", "வயிறு", "நெஞ்செரிச்சல்"]):
            return (
                "💊 நெஞ்செரிச்சல் & அஜீரணத்திற்கான பொதுவான வழிகாட்டுதல்:\n\n"
                "1. Antacid திரவம் (எ.கா: Gelusil / Digene):\n"
                "• உணவுக்குப் பின் அல்லது நெஞ்செரிச்சல் உள்ள போது 1-2 ஸ்பூன் அருந்தலாம்.\n"
                "2. ORS கரைசல்:\n"
                "• பேதி அல்லது வாந்தி இருந்தால் உடனே ORS நீரை சிறிது சிறிதாக குடிக்கவும்.\n\n"
                "❌ செய்யக்கூடாதவை: காரமான, எண்ணெயில் பொரித்த உணவுகளைத் தவிர்க்கவும்."
            ) + disclaimer
        else:
            return (
                "💊 பொதுவான முதலுதவி மருந்து வழிகாட்டுதல்:\n\n"
                "• லேசான வலி/காய்ச்சலுக்கு: Paracetamol.\n"
                "• சளி/தும்மலுக்கு: நீராவி பிடித்தல் மற்றும் வெந்நீர் அருந்துதல்.\n"
                "• நீரிழப்புக்கு: ORS கரைசல்.\n\n"
                "குறிப்பிட்ட மருந்து மற்றும் சரியான அளவை அறிய அருகில் உள்ள மருத்துவரை அணுகவும்."
            ) + disclaimer
    else:
        disclaimer = "\n\n⚠️ Safety Notice: This is supportive OTC education, not a personal prescription. Always confirm with a qualified doctor or licensed pharmacist before taking any medication."
        if any(w in c for w in ["fever", "pain", "chills", "ache"]):
            return (
                "💊 Common OTC Supportive Medications for Fever & Discomfort:\n\n"
                "1. Paracetamol / Acetaminophen (e.g., Dolo 650, Crocin, Tylenol):\n"
                "• Typical Adult Dose: 500mg - 650mg every 6 to 8 hours as needed.\n"
                "• Maximum Limit: Do NOT exceed 3000mg (3g) in 24 hours to protect liver health.\n"
                "• Take after a light snack or meal; avoid on a completely empty stomach.\n\n"
                "2. ORS (Oral Rehydration Salts) & Electrolytes:\n"
                "• Restores vital fluids lost to fever sweating and high body temperature.\n\n"
                "❌ Critical Safety Precautions:\n"
                "• Do NOT self-prescribe antibiotics without a doctor's lab confirmation.\n"
                "• Never give Aspirin to children or adolescents under 18 (risk of Reye's syndrome)."
            ) + disclaimer
        elif any(w in c for w in ["stomach", "acidity", "indigestion", "heartburn", "gastric"]):
            return (
                "💊 Common OTC Options for Acidity & Upset Stomach:\n\n"
                "1. Antacid Syrups / Chewables (e.g., Digene, Gelusil, Mylanta):\n"
                "• Neutralizes excess stomach acid; take 10-15 ml after meals or at onset of burning.\n"
                "2. Electrolyte / ORS Packets:\n"
                "• Essential if experiencing loose stools or nausea to prevent dangerous dehydration.\n\n"
                "❌ Dietary Precaution: Avoid spicy, fried foods, alcohol, and caffeine."
            ) + disclaimer
        else:
            return (
                "💊 General OTC Relief Principles:\n\n"
                "• Mild pain/fever: Paracetamol.\n"
                "• Dehydration/weakness: ORS solution or tender coconut water.\n"
                "• Nasal congestion: Steam inhalation and saline nasal spray.\n\n"
                "Always check with a physician if symptoms do not improve in 48 hours."
            ) + disclaimer


@tool
def get_first_aid_guidance(situation: str, language: str = "English") -> str:
    """
    Provide step-by-step basic first aid guidance for common situations.
    Use for cuts, burns, sprains, fever, fainting, nosebleed, or choking.
    """
    s = situation.lower()

    if any(w in s for w in ["cut", "wound", "bleeding", "scratch", "bleed", "வெட்டு", "காயம்", "இரத்தம்"]):
        if language == "Tamil":
            return (
                "🩹 வெட்டு காயத்திற்கான விரைவு முதலுதவி:\n\n"
                "1. அழுத்தம்: சுத்தமான துணியால் காயத்தை 10-15 நிமிடம் அழுத்திப் பிடிக்கவும்.\n"
                "2. கழுவுதல்: சுத்தமான ஓடும் நீரில் கழுவவும் (சோப்பு ஓரங்களில் மட்டும்).\n"
                "3. கிருமி நாசினி: Dettol அல்லது Betadine போன்ற ஆன்டிசெப்டிக் தடவவும்.\n"
                "4. கட்டு: சுத்தமான பாண்டேஜ் போடவும்.\n\n"
                "⚠️ மருத்துவரிடம் செல்ல வேண்டிய நேரம்: காயம் ஆழமாக இருந்தால் அல்லது இரத்தம் நிற்காவிட்டால்."
            )
        else:
            return (
                "🩹 First Aid for Cuts & Wounds:\n\n"
                "1. Direct Pressure: Press firmly with a clean cloth for 10-15 mins until bleeding stops.\n"
                "2. Cleanse: Rinse thoroughly with cool tap water.\n"
                "3. Antiseptic: Apply Betadine or antiseptic ointment.\n"
                "4. Dress: Cover with a sterile bandage.\n\n"
                "⚠️ Seek Doctor: If cut is deep, gaping, or bleeding does not stop after 15 mins."
            )

    elif any(w in s for w in ["burn", "scald", "fire", "hot", "தீக்காயம்", "வெந்நீர்", "சுட்டு"]):
        if language == "Tamil":
            return (
                "🔥 தீக்காயத்திற்கான விரைவு முதலுதவி:\n\n"
                "1. குளிர்வித்தல்: உடனடியாக குளிர்ந்த ஓடும் நீரில் 20 நிமிடங்கள் வைக்கவும் (ஐஸ் வேண்டாம்).\n"
                "2. தொடாதீர்கள்: கொப்புளங்களை உடைக்கவோ தோலை உரிக்கவோ கூடாது.\n"
                "3. வேண்டாம்: வெண்ணெய், பேஸ்ட், எண்ணெய் எதையும் தடவாதீர்கள்.\n"
                "4. மூடுதல்: சுத்தமான ஈரத் துணியால் லேசாக மூடவும்."
            )
        else:
            return (
                "🔥 First Aid for Burns:\n\n"
                "1. Cool Immediately: Hold under cool running water for 20 minutes (do NOT use ice).\n"
                "2. Leave Blisters Alone: Never pop or peel blistered skin.\n"
                "3. No Home Remedies: Avoid toothpaste, butter, or oils.\n"
                "4. Protect: Cover loosely with a clean, sterile damp dressing."
            )

    elif any(w in s for w in ["fever", "temperature", "chills", "காய்ச்சல்", "உடல் வெப்பம்"]):
        if language == "Tamil":
            return (
                "🌡️ காய்ச்சலுக்கான முதலுதவி வழிகாட்டி:\n\n"
                "1. நீரேற்றம்: நிறைய தண்ணீர், ORS, இளநீர் குடிக்கவும்.\n"
                "2. ஒத்தடம்: நெற்றியில் சாதாரண குளிர்ந்த நீர் துணியால் ஒத்தடம் கொடுக்கவும்.\n"
                "3. ஆடை: மெல்லிய பருத்தி ஆடை அணியவும் (கம்பளி போர்த்த வேண்டாம்).\n"
                "4. மருந்து: பெரியவர்களுக்கு Paracetamol (Dolo 650) தேவைப்பட்டால் உட்கொள்ளலாம்.\n"
                "5. ஓய்வு: முழு ஓய்வு மிக முக்கியம்."
            )
        else:
            return (
                "🌡️ First Aid & Care for Fever:\n\n"
                "1. Hydrate Heavily: Drink water, ORS, broths, or coconut water frequently.\n"
                "2. Cool Compress: Place a damp, lukewarm cloth on the forehead.\n"
                "3. Light Clothing: Dress in breathable, loose cotton garments.\n"
                "4. Supportive Relief: Paracetamol (e.g., Dolo 650) as appropriate for age.\n"
                "5. Rest: Restrict physical exertion to conserve immune defense."
            )

    else:
        if language == "Tamil":
            return "பொது முதலுதவி: வெட்டு, தீக்காயம், காய்ச்சல் அல்லது பிசக்கல் குறித்த குறிப்பிட்ட ஆலோசனையை என்னிடம் கேட்கலாம்."
        else:
            return "General First Aid: You can ask for rapid step-by-step guidance on cuts, burns, sprains, or fever management."


@tool
def explain_possible_causes(symptom: str, language: str = "English") -> str:
    """Explain possible causes of symptoms with non-diagnostic disclaimers."""
    s = symptom.lower()
    if language == "Tamil":
        disclaimer = "\n\n📋 குறிப்பு: இவை பொதுவான சாத்தியங்கள் மட்டுமே. உறுதியான நோயறிதலுக்கு மருத்துவரை அணுகவும்."
        if "தலைவலி" in s or "headache" in s:
            return "🤕 தலைவலிக்கான காரணங்கள்: நீரிழப்பு, தூக்கமின்மை, மன அழுத்தம், சைனஸ் அல்லது கண் சிரமம்." + disclaimer
        elif "காய்ச்சல்" in s or "fever" in s:
            return "🌡️ காய்ச்சலுக்கான காரணங்கள்: வைரஸ் தொற்று, பாக்டீரியா தொற்று, சிறுநீரக தொற்று அல்லது மலேரியா/டெங்கு." + disclaimer
        else:
            return f"🔍 '{symptom}' காரணங்கள்: தொற்று, தசை அழுத்தம் அல்லது ஒவ்வாமை காரணமாக இருக்கலாம்." + disclaimer
    else:
        disclaimer = "\n\n📋 Note: These are informational possibilities, not a definitive diagnosis. Please consult a qualified doctor."
        if "headache" in s:
            return "🤕 Headache Causes: Dehydration, sleep deficit, tension, eyestrain, or sinus congestion." + disclaimer
        elif "fever" in s:
            return "🌡️ Fever Causes: Viral infection, seasonal flu, bacterial infection, or mosquito-borne illnesses." + disclaimer
        else:
            return f"🔍 Causes for '{symptom}': Could stem from viral activity, inflammatory response, or lifestyle strain." + disclaimer


@tool
def get_general_health_tips(topic: str, language: str = "English") -> str:
    """Provide preventive health guidance on hydration, sleep, and lifestyle."""
    t = topic.lower()
    if language == "Tamil":
        return "🌿 ஆரோக்கியக் குறிப்பு: தினமும் 8-10 டம்ளர் தண்ணீர் குடிக்கவும், 7-8 மணி நேரம் தூங்கவும், சத்தான உணவுகளை உட்கொள்ளவும்."
    else:
        return "🌿 Wellness Tip: Drink 2.5-3 liters of clean water daily, secure 7-8 hours of uninterrupted sleep, and maintain balanced nutrition."


@tool
def get_wound_treatment_guide(wound_type: str, language: str = "English") -> str:
    """
    Hospitalization-grade step-by-step emergency wound treatment and stabilization tutorial.
    Designed for remote areas, villages, or emergencies when a hospital is hours away.
    Handles minor cuts, severe arterial bleeding, puncture wounds, burns, animal/snake bites, and fracture splinting.
    """
    w = wound_type.lower()
    is_ta = language == "Tamil"

    if any(k in w for k in ["severe", "arterial", "heavy", "gushing", "இரத்தப்போக்கு", "அதிக இரத்தம்"]):
        if is_ta:
            return (
                "🚨 தீவிர இரத்தப்போக்கு கட்டுப்படுத்துதல் (Emergency Severe Bleeding Control):\n\n"
                "மருத்துவமனை தொலைவில் இருக்கும்போது உடனடியாக செய்ய வேண்டிய படிகள்:\n\n"
                "1. நேரடி அழுத்தம் (Direct Firm Pressure):\n"
                "• சுத்தமான தடிமனான துணி அல்லது காஸ் துணியை எடுத்து, காயம் உள்ள இடத்தில் உள்ளங்கையால் முழு பலத்துடன் 10-15 நிமிடங்கள் விடாமல் அழுத்திப் பிடிக்கவும்.\n"
                "• துணி இரத்தத்தால் நனைந்தால், அதை அகற்றாமல் அதன் மேல் கூடுதல் துணியை வைத்து அழுத்தவும்.\n\n"
                "2. காயமடைந்த பகுதியை உயர்த்துதல் (Elevation):\n"
                "• காயம் கை அல்லது காலில் இருந்தால், அதை இதய மட்டத்திற்கு மேல் உயர்த்தி வைக்கவும்.\n\n"
                "3. இறுக்கமான அழுத்தக்கட்டு (Pressure Bandage):\n"
                "• இரத்தப்போக்கு குறைந்ததும், சுத்தமான ரோலர் பேண்டேஜ் மூலம் உறுதியாக கட்டவும்.\n\n"
                "4. டூர்னிகெட் நெறிமுறை (Tourniquet - கை/கால் தீவிர இரத்தப்போக்கிற்கு மட்டும்):\n"
                "• இரத்தம் நிற்காமல் பீறிட்டால், காயத்திற்கு 2-3 அங்குலம் மேலே அகலமான துணி அல்லது பெல்ட்டால் இறுகக் கட்டி, நேரம் குறித்துக் கொள்ளவும் (அதிகபட்சம் 2 மணி நேரம்).\n\n"
                "⚠️ உடனே வாகனத்தை ஏற்பாடு செய்து அருகிலுள்ள அரசு ஆரம்ப சுகாதார நிலையம் (PHC) அல்லது மருத்துவமனைக்கு நோயாளியை கொண்டு செல்லவும்."
            )
        else:
            return (
                "🚨 Severe / Arterial Bleeding Control (Hospitalization-Grade Emergency Protocol):\n\n"
                "When emergency transport or hospital is hours away, follow these stabilization steps:\n\n"
                "1. Direct Firm Continuous Pressure:\n"
                "• Place a thick sterile gauze pad or clean cloth directly over the bleeding site.\n"
                "• Press down with maximum palm pressure continuously for 10-15 minutes without lifting to check.\n"
                "• If blood soaks through, DO NOT remove the bottom cloth—add more layers on top and press harder.\n\n"
                "2. Elevation:\n"
                "• If on an arm or leg, elevate the limb above heart level to reduce gravitational blood pressure.\n\n"
                "3. Pressure Bandage:\n"
                "• Secure the dressing tightly with an elastic or roller bandage.\n\n"
                "4. Emergency Tourniquet (Extremities Only, Life-Threatening Bleed):\n"
                "• If blood continues spurting from a limb, apply a commercial or improvised tourniquet (wide cloth) 2-3 inches above the wound. Tighten until bleeding stops. Record the exact application time.\n\n"
                "⚠️ Non-negotiable: Arrange immediate transport to the nearest hospital or Primary Health Center (PHC)."
            )

    elif any(k in w for k in ["puncture", "nail", "rusty", "ஆணி", "துளைக் காயம்"]):
        if is_ta:
            return (
                "🩹 ஆணி / முள் குத்திய காயம் (Puncture Wound Protocol):\n\n"
                "1. ஓடும் நீரில் கழுவுதல்: காயத்தை 5-10 நிமிடங்கள் சாதாரண ஓடும் நீரில் சோப்பு கொண்டு நன்றாகக் கழுவவும்.\n"
                "2. அழுத்த வேண்டாம்: கிருமிகளை உள்ளே தள்ளும் என்பதால் ஆழமாக அழுத்தக் கூடாது.\n"
                "3. கிருமிநாசினி: Betadine (Povidone-Iodine 5%) திரவத்தை காயத்தின் மேல் தடவவும்.\n"
                "4. பாதுகாப்பு கட்டு: சுத்தமான காற்று புகும் பேண்டேஜ் போடவும்.\n\n"
                "⚠️ டெட்டனஸ் எச்சரிக்கை (Tetanus Alert): துருப்பிடித்த ஆணி குத்தியிருந்தால் 24 மணி நேரத்திற்குள் TT (Tetanus Toxoid) தடுப்பூசி போடுவது கட்டாயம்!"
            )
        else:
            return (
                "🩹 Puncture Wounds & Rusty Nails Protocol:\n\n"
                "1. Thorough Irrigation: Wash under running tap water with mild soap for 5-10 minutes to flush out dirt and debris.\n"
                "2. Do Not Dig: Do not probe deep into the wound with needles or tweezers.\n"
                "3. Disinfect: Apply Povidone-Iodine 5% (Betadine) liberally.\n"
                "4. Sterile Dressing: Cover lightly with a sterile bandage.\n\n"
                "⚠️ Critical Tetanus Alert: If the object was dirty, soil-covered, or rusty, a Tetanus Toxoid (TT) injection within 24 hours is mandatory."
            )

    elif any(k in w for k in ["snake", "animal", "dog", "bite", "நாய் கடி", "பாம்பு கடி"]):
        if is_ta:
            return (
                "🐍 பாம்பு / நாய் கடி முதலுதவி (Snake & Animal Bite Emergency):\n\n"
                "🐕 நாய் அல்லது விலங்கு கடித்தால்:\n"
                "1. உடனடியாக காயத்தை ஓடும் குழாய் நீரில் சோப்பு போட்டு 15 நிமிடங்கள் இடைவிடாமல் கழுவவும் (இது ரேபிஸ் வைரஸை 70% அழிக்கிறது).\n"
                "2. Betadine தடவவும். காயத்தை தைக்கவோ மூடவோ கூடாது.\n"
                "3. உடனே மருத்துவமனை சென்று ரேபிஸ் தடுப்பூசி (Anti-Rabies Vaccine) போடவும்.\n\n"
                "🐍 பாம்பு கடித்தால்:\n"
                "1. நோயாளியை முற்றிலும் அசையாமல் அமைதியாக படுக்க வைக்கவும் (பதற்றம் விஷத்தை வேகமாக பரப்பும்).\n"
                "2. கடித்த இடத்தை இதய மட்டத்திற்கு கீழே வைக்கவும்.\n"
                "3. இறுக்கமான மோதிரம், வளையல், காலணிகளை உடனே கழற்றவும்.\n"
                "❌ செய்யக்கூடாதவை: பிளேடால் கீறக் கூடாது, வாயால் விஷத்தை உறிஞ்சக் கூடாது, டூர்னிகெட் இறுக்கிக் கட்டக் கூடாது!\n"
                "🚑 அருகிலுள்ள Anti-Snake Venom (ASV) உள்ள அரசு மருத்துவமனைக்கு உடனடியாக கொண்டு செல்லவும்."
            )
        else:
            return (
                "🐍 Snake & Animal Bite Clinical Stabilization Protocol:\n\n"
                "🐕 For Dog / Mammal Bites:\n"
                "1. Flush immediately under running tap water with soap for a FULL 15 MINUTES. This mechanical wash neutralizes the rabies virus.\n"
                "2. Apply Povidone Iodine. Do NOT suture or tightly bandage.\n"
                "3. Proceed immediately to a clinic for the Anti-Rabies Vaccine (ARV) series.\n\n"
                "🐍 For Snake Bites:\n"
                "1. Keep patient completely still and calm; physical movement accelerates venom circulation.\n"
                "2. Immobilize the bitten limb with a splint at or slightly below heart level.\n"
                "3. Remove tight rings, bangles, or shoes before swelling begins.\n"
                "❌ ABSOLUTE DONT'S: Do NOT cut the wound, do NOT suck venom, do NOT apply electric shocks, do NOT tie a tight tourniquet.\n"
                "🚑 Rush immediately to the nearest government hospital stocked with Anti-Snake Venom (ASV)."
            )

    elif any(k in w for k in ["burn", "தீக்காயம்"]):
        if is_ta:
            return (
                "🔥 தீவிர தீக்காய சிகிச்சை வழிகாட்டி (Burn Emergency Care):\n\n"
                "1. 20 நிமிட குளிர்வித்தல்: உடனடியாக சாதாரண ஓடும் குளிர்ந்த நீரில் 20 நிமிடங்கள் வைக்கவும் (ஐஸ் அல்லது குளிர்ந்த பால் பயன்படுத்த வேண்டாம்).\n"
                "2. ஆடைகளை அகற்றுதல்: தோலில் ஒட்டாத தளர்வான துணிகளை மெதுவாக அகற்றவும். ஒட்டியிருந்தால் இழுக்க வேண்டாம்.\n"
                "3. மருந்து: Silver Sulfadiazine (சில்வர் சல்படயாசின் 1%) கிரீம் லேசாக பூசவும்.\n"
                "4. கொப்புளங்கள்: கொப்புளங்களை ஒருபோதும் உடைக்கக் கூடாது.\n"
                "5. மூடுதல்: சுத்தமான ஈரமில்லாத மலட்டுத் துணியால் லேசாக மூடவும்.\n"
                "⚠️ தீக்காயம் உள்ளங்கை அளவை விட பெரிதாக இருந்தாலோ அல்லது முகம், பிறப்புறுப்பில் இருந்தாலோ உடனடியாக மருத்துவமனைக்கு செல்லவும்."
            )
        else:
            return (
                "🔥 Burn Emergency & Stabilization Tutorial:\n\n"
                "1. Immediate Cooling: Irrigate under cool running tap water for a full 20 minutes. Never use ice, ice water, or butter.\n"
                "2. Clear Constrictions: Gently remove rings, belts, or loose clothing before edema sets in. Never peel fabric stuck to burnt skin.\n"
                "3. Topical Relief: Apply Silver Sulfadiazine 1% cream or sterile petroleum dressing.\n"
                "4. Blister Care: Never puncture or de-roof blisters.\n"
                "5. Sterile Protection: Drape loosely with sterile cling wrap or non-adherent dressing.\n"
                "⚠️ Hospital Referral: Burns larger than the patient's palm, electrical burns, chemical burns, or facial involvement require emergency hospitalization."
            )

    else:
        if is_ta:
            return (
                "🩹 பொதுவான வெட்டுக் காயம் பராமரிப்பு (Standard Wound Cleaning):\n\n"
                "1. கைகளை சோப்பால் கழுவவும்.\n"
                "2. காயத்தை சுத்தமான நீரில் கழுவி மணல், அழுக்கை நீக்கவும்.\n"
                "3. Betadine அல்லது Neosporin கிருமிநாசினி பூசவும்.\n"
                "4. மலட்டு காஸ் (Sterile Gauze) வைத்து பேண்டேஜ் போடவும்.\n"
                "5. தினமும் ஒரு முறை கட்டு மாற்றி, சீழ் அல்லது வீக்கம் உள்ளதா என கவனிக்கவும்."
            )
        else:
            return (
                "🩹 Standard Wound Dressing & Healing Protocol:\n\n"
                "1. Wash hands thoroughly with soap.\n"
                "2. Irrigate wound bed with clean water or sterile saline to remove particulate debris.\n"
                "3. Apply Povidone-Iodine 5% or Bacitracin/Neosporin ointment.\n"
                "4. Cover with a sterile gauze pad and secure with breathable medical tape.\n"
                "5. Change dressing daily or whenever damp. Watch for redness, warmth, or pus indicating infection."
            )


@tool
def get_essential_medicine_list(category: str = "all", language: str = "English") -> str:
    """
    Catalog of essential OTC medicines and first-aid supplies to stock at home.
    Crucial for remote communities and locations where medical pharmacies are distant.
    Includes indications, dosages, contraindications, and storage.
    """
    is_ta = language == "Tamil"

    if is_ta:
        return (
            "📦 தொலைதூர வீடுகளுக்கான அத்தியாவசிய முதலுதவி & OTC மருந்துகள் பட்டியல்:\n\n"
            "1. காய்ச்சல் & வலி நிவாரணம்:\n"
            "• Paracetamol (Dolo 650mg / Calpol 500mg): காய்ச்சல் மற்றும் உடல் வலிக்கு. பெரியவர்களுக்கு 6-8 மணி நேரத்திற்கு ஒரு முறை (அதிகபட்சம் 3000mg/நாள்).\n\n"
            "2. காயம் & இரத்தப்போக்கு முதலுதவி:\n"
            "• Povidone Iodine 5% (Betadine): சிறந்த கிருமிநாசினி திரவம் மற்றும் களிம்பு.\n"
            "• Sterile Gauze Pads (மலட்டு துணி 2x2, 4x4 அங்குலம்): இரத்தத்தை நிறுத்தவும் கட்டு போடவும்.\n"
            "• Micropore Medical Tape & Roller Bandage: கட்டுகளை உறுதியாகப் பொருத்த.\n"
            "• Bandage Scissors & Tweezers: முள் அல்லது அழுக்கை அகற்ற.\n\n"
            "3. வயிற்றுப்போக்கு & நீரிழப்பு பாதுகாப்பு:\n"
            "• WHO-ORS பாக்கெட்டுகள் (Oral Rehydration Salts): வாந்தி, பேதிக்கு உயிர்காக்கும் எலக்ட்ரோலைட்.\n"
            "• Antacid (Digene / Gelusil): நெஞ்செரிச்சல் மற்றும் அசிடிட்டிக்கு.\n\n"
            "4. தீக்காயம் & ஒவ்வாமை:\n"
            "• Silver Sulfadiazine 1% Ointment: தீக்காயங்களில் தொற்று ஏற்படாமல் காக்க.\n"
            "• Cetirizine 10mg: வண்டு கடி, தும்மல் மற்றும் தோல் ஒவ்வாமைக்கு (இரவு 1 மாத்திரை).\n\n"
            "5. அத்தியாவசிய வீட்டுக் கருவிகள்:\n"
            "• Digital Clinical Thermometer (வெப்பமானி)\n"
            "• Pulse Oximeter (இரத்த ஆக்சிஜன் மற்றும் நாடித் துடிப்பு பார்க்க)\n"
            "• BP Monitor (இரத்த அழுத்த மானி)\n\n"
            "⚠️ மருந்துகளை குழந்தைகளின் கைக்கு எட்டாத உலர்ந்த, குளிர்ந்த இடத்தில் வைக்கவும். காலாவதி தேதியை தவறாமல் பரிசோதிக்கவும்."
        )
    else:
        return (
            "📦 Remote Area Essential Medicine & First-Aid Home Stocking Checklist:\n\n"
            "1. Fever, Pain & Inflammation:\n"
            "• Paracetamol (500mg / 650mg): Safe antipyretic & analgesic. Dose: 500-650mg every 6-8 hrs as needed. Max 3000mg/day.\n\n"
            "2. Wound Treatment & Antiseptics:\n"
            "• Povidone-Iodine 5% Solution & Ointment (Betadine): Gold standard broad-spectrum antiseptic.\n"
            "• Sterile Gauze Pads (2x2 and 4x4 inches): For bleeding control and sterile dressing.\n"
            "• Roller Bandages & Micropore Tape: For pressure dressings and securing bandages.\n"
            "• Bandage Shears & Splinter Forceps.\n\n"
            "3. Dehydration & Gastrointestinal:\n"
            "• WHO-Formula ORS (Oral Rehydration Salts) Packets: Life-saving electrolyte packets for diarrhea, vomiting, or heat exhaustion.\n"
            "• Antacids (Gelusil / Digene chewables or liquid): For acute acidity and gastric burning.\n\n"
            "4. Burns, Bites & Allergies:\n"
            "• Silver Sulfadiazine 1% Cream (Burnol / Silvadene): For 1st & 2nd degree burn healing.\n"
            "• Cetirizine 10mg: Non-sedating antihistamine for insect stings, rash, and acute allergy (1 tablet at bedtime).\n"
            "• Calamine Lotion: For soothing itchy rashes and bug bites.\n\n"
            "5. Vital Diagnostic Instruments:\n"
            "• Digital Clinical Thermometer (oral/axillary).\n"
            "• Fingertip Pulse Oximeter (SpO2 % & Heart Rate).\n"
            "• Automatic Arm Blood Pressure Monitor.\n\n"
            "⚠️ Storage: Store in an airtight, moisture-proof box away from direct sunlight. Check expiration dates quarterly."
        )


@tool
def generate_doctor_summary(patient_vitals_summary: str, language: str = "English") -> str:
    """
    Synthesize recorded daily health logs into a professional clinical handover summary
    for an attending physician, primary health center (PHC) medical officer, or tele-consultant.
    """
    is_ta = language == "Tamil"
    if is_ta:
        return (
            f"📋 மாதாந்திர மருத்துவ அறிக்கை சுருக்கம் (Monthly Clinical Summary for Doctor):\n\n"
            f"{patient_vitals_summary}\n\n"
            f"மருத்துவர் கவனத்திற்கு:\n"
            f"• நோயாளி தொலைதூர பகுதியில் வசிக்கிறார்.\n"
            f"• மேலே பதிவு செய்யப்பட்டுள்ள இரத்த அழுத்தம், சர்க்கரை அளவு மற்றும் முக்கிய அறிகுறிகளை பரிசோதித்து மேலதிக மருந்துகள் பரிந்துரைக்கவும்."
        )
    else:
        return (
            f"📋 Monthly Clinical Vitals & Symptom Handover Summary for Attending Physician:\n\n"
            f"{patient_vitals_summary}\n\n"
            f"Clinical Attention Points:\n"
            f"• Patient resides in a remote location with limited immediate access to acute tertiary care.\n"
            f"• Review vitals stability (BP trends, glucose fluctuations, lowest SpO2) and cross-reference with recorded symptom episodes for medication adjustments."
        )

