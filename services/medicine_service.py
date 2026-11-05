# services/medicine_service.py
"""
Essential Home Medicine Kit & Diagnostic Tools Service
Bilingual catalog of over-the-counter emergency medicines and devices.
"""

ESSENTIAL_MEDS = [
    {
        "id": "betadine",
        "category": "wound",
        "icon": "🩹",
        "nameEn": "Povidone-Iodine 5% (Betadine)",
        "nameTa": "Betadine 5% (பொவிடோன் அயோடின்)",
        "typeEn": "Antiseptic Liquid & Ointment",
        "typeTa": "கிருமிநாசினி திரவம் & கிரீம்",
        "doseEn": "Apply directly on cleaned cuts, grazes, or minor burns.",
        "doseTa": "கழுவப்பட்ட காயங்கள், கீறல்கள் மீது நேரடியாக பூசவும்.",
        "limitEn": "External use only. Avoid in iodine allergy.",
        "limitTa": "வெளிப்புற பயன்பாட்டிற்கு மட்டும். அயோடின் ஒவ்வாமை இருந்தால் தவிர்க்கவும்.",
        "cautionEn": "Gold standard antiseptic to prevent bacterial infection in remote homes.",
        "cautionTa": "தொற்று ஏற்படாமல் காக்கும் மிக முக்கியமான முதலுதவி கிருமிநாசினி."
    },
    {
        "id": "gauze",
        "category": "wound",
        "icon": "📦",
        "nameEn": "Sterile Gauze Pads & Micropore Tape",
        "nameTa": "மலட்டு காஸ் துணி & மெடிக்கல் டேப்",
        "typeEn": "Wound Dressing Material",
        "typeTa": "கட்டுப் போடும் மருத்துவ துணி",
        "doseEn": "2x2 inch & 4x4 inch sterile pads for bleeding control and dressing.",
        "doseTa": "இரத்தப்போக்கை நிறுத்தவும் கட்டு போடவும் பயன்படும் மலட்டு துணிகள்.",
        "limitEn": "Keep in sealed waterproof pack until use.",
        "limitTa": "ஈரம் படாத காற்று புகாத பாக்கெட்டில் வைக்கவும்.",
        "cautionEn": "Never use unwashed dirty household cloth on open bleeding flesh.",
        "cautionTa": "இரத்தம் வரும் காயத்தின் மேல் அசுத்தமான துணிகளை வைக்கக் கூடாது."
    },
    {
        "id": "paracetamol",
        "category": "fever",
        "icon": "🌡️",
        "nameEn": "Paracetamol (Dolo 650 / Calpol 500)",
        "nameTa": "Paracetamol (Dolo 650 / பாராசிட்டமால்)",
        "typeEn": "Antipyretic & Pain Reliever",
        "typeTa": "காய்ச்சல் மற்றும் வலி நிவாரணி",
        "doseEn": "Adults: 500mg-650mg every 6-8 hours after food.",
        "doseTa": "பெரியவர்கள்: 500mg-650mg தேவைப்பட்டால் 6-8 மணி நேரத்திற்கு ஒரு முறை.",
        "limitEn": "Max 3000mg (3g) per 24 hours to protect liver.",
        "limitTa": "ஒரு நாளில் 3000mg-க்கு மேல் உட்கொள்ளக் கூடாது (கல்லீரல் பாதுகாப்பு).",
        "cautionEn": "Safe for fever and headaches. Avoid combining multiple paracetamol brands.",
        "cautionTa": "காய்ச்சல் மற்றும் தலைவலிக்கு பாதுகாப்பானது. வெறும் வயிற்றில் சாப்பிட வேண்டாம்."
    },
    {
        "id": "ors",
        "category": "stomach",
        "icon": "💧",
        "nameEn": "WHO-Formula ORS (Oral Rehydration Salts)",
        "nameTa": "WHO-ORS எலக்ட்ரோலைட் பாக்கெட்",
        "typeEn": "Electrolyte Life-Saver",
        "typeTa": "உயிர் காக்கும் உப்பு-சர்க்கரை கரைசல்",
        "doseEn": "Mix 1 sachet in exactly 1 liter of clean drinking water. Sip continuously.",
        "doseTa": "1 பாக்கெட்டை 1 லிட்டர் சுத்தமான நீரில் கலந்து சிறிது சிறிதாக குடிக்கவும்.",
        "limitEn": "Drink within 24 hours of preparation. Discard remainder.",
        "limitTa": "கலந்த 24 மணி நேரத்திற்குள் குடிக்கவும். மீதத்தை கொட்டி விடவும்.",
        "cautionEn": "Prevents death from dehydration during diarrhea, vomiting, and high fever.",
        "cautionTa": "வாந்தி, பேதி மற்றும் காய்ச்சலின் போது ஏற்படும் நீரிழப்பைத் தடுத்து உயிர் காக்கும்."
    },
    {
        "id": "antacid",
        "category": "stomach",
        "icon": "🤢",
        "nameEn": "Antacid (Digene / Gelusil)",
        "nameTa": "Antacid சிரப் / மாத்திரை (டைஜீன்)",
        "typeEn": "Acidity & Heartburn Relief",
        "typeTa": "நெஞ்செரிச்சல் மற்றும் அசிடிட்டி நிவாரணம்",
        "doseEn": "10-15 ml liquid or 1-2 chewable tablets after meals.",
        "doseTa": "உணவுக்குப் பின் 10-15 மிலி திரவம் அல்லது 1-2 மெல்லும் மாத்திரைகள்.",
        "limitEn": "Do not exceed 4 times daily.",
        "limitTa": "ஒரு நாளில் 4 முறைக்கு மேல் உட்கொள்ள வேண்டாம்.",
        "cautionEn": "Relieves indigestion and burning chest discomfort.",
        "cautionTa": "அஜீரணம், வாயு மற்றும் நெஞ்செரிச்சலை உடனடியாகக் கட்டுப்படுத்தும்."
    },
    {
        "id": "burnol",
        "category": "allergy",
        "icon": "🔥",
        "nameEn": "Silver Sulfadiazine 1% (Burnol Cream)",
        "nameTa": "Silver Sulfadiazine 1% (தீக்காய கிரீம்)",
        "typeEn": "Topical Antibacterial Burn Cream",
        "typeTa": "தீக்காய கிருமி தடுப்பு களிம்பு",
        "doseEn": "Gently spread a sterile 1-2 mm layer over cooled burns.",
        "doseTa": "குளிர்விக்கப்பட்ட தீக்காயத்தின் மேல் 1-2 மிமீ தடிமனில் மெதுவாக பூசவும்.",
        "limitEn": "Not for pregnant women near term or infants under 2 months.",
        "limitTa": "கர்ப்பிணிகள் மற்றும் 2 மாதத்திற்குட்பட்ட குழந்தைகளுக்கு தவிர்க்கவும்.",
        "cautionEn": "Prevents dangerous hospital-acquired wound infections in burn cases.",
        "cautionTa": "தீக்காயங்களில் கொப்புளங்கள் மற்றும் சீழ் தொற்று ஏற்படாமல் காக்கும்."
    },
    {
        "id": "cetirizine",
        "category": "allergy",
        "icon": "🐝",
        "nameEn": "Cetirizine 10mg",
        "nameTa": "Cetirizine 10mg (சிட்ரிசின்)",
        "typeEn": "Antihistamine / Allergy Relief",
        "typeTa": "ஒவ்வாமை மற்றும் அரிப்பு மாத்திரை",
        "doseEn": "Adults: 1 tablet (10mg) once daily at bedtime.",
        "doseTa": "பெரியவர்கள்: இரவு படுக்கும் முன் 1 மாத்திரை (10mg).",
        "limitEn": "May cause slight drowsiness. Avoid driving.",
        "limitTa": "லேசான தூக்கக் கலக்கம் வரலாம். வாகனம் ஓட்டுவதைத் தவிர்க்கவும்.",
        "cautionEn": "Essential for insect stings, sudden skin rashes, and allergic sneezing.",
        "cautionTa": "வண்டு கடி, தோல் தடிப்புகள் மற்றும் ஒவ்வாமை தும்மலுக்கு மிகச் சிறந்தது."
    },
    {
        "id": "thermometer",
        "category": "tools",
        "icon": "🌡️",
        "nameEn": "Digital Clinical Thermometer",
        "nameTa": "டிஜிட்டல் வெப்பமானி (Thermometer)",
        "typeEn": "Diagnostic Device",
        "typeTa": "உடல் வெப்பநிலை அளக்கும் கருவி",
        "doseEn": "Place under armpit or tongue until beep. Normal: 97.7°F - 99.0°F.",
        "doseTa": "அக்குளில் அல்லது நாக்கின் அடியில் வைத்து பீப் சத்தம் வரை வைக்கவும்.",
        "limitEn": "Disinfect tip with alcohol before and after each use.",
        "limitTa": "பயன்படுத்துவதற்கு முன்பும் பின்பும் ஆல்கஹால் துணியால் துடைக்கவும்.",
        "cautionEn": "Never guess fever with bare hands—accurate readings prevent febrile convulsions.",
        "cautionTa": "கையால் தொட்டு காய்ச்சலை யூகிக்காமல் சரியான வெப்பநிலையை அறிய உதவும்."
    },
    {
        "id": "oximeter",
        "category": "tools",
        "icon": "🩺",
        "nameEn": "Fingertip Pulse Oximeter",
        "nameTa": "பல்ஸ் ஆக்ஸிமீட்டர் (Pulse Oximeter)",
        "typeEn": "SpO2 & Heart Rate Monitor",
        "typeTa": "ஆக்சிஜன் & நாடித் துடிப்பு கருவி",
        "doseEn": "Clip on index finger while resting. Normal SpO2: 95% - 100%.",
        "doseTa": "ஆள்காட்டி விரலில் பொருத்தவும். இயல்பான ஆக்சிஜன்: 95% - 100%.",
        "limitEn": "SpO2 below 94% indicates urgent need for supplemental oxygen.",
        "limitTa": "94%-க்கு கீழ் சென்றால் உடனடியாக மருத்துவமனை செல்ல வேண்டும்.",
        "cautionEn": "Vital for respiratory infections, pneumonia, and elderly care in remote homes.",
        "cautionTa": "நுரையீரல் தொற்று, சளி மற்றும் முதியோர்களின் ஆக்சிஜன் அளவை கண்காணிக்க உதவும்."
    },
    {
        "id": "bp-monitor",
        "category": "tools",
        "icon": "💓",
        "nameEn": "Automatic Arm Blood Pressure Monitor",
        "nameTa": "டிஜிட்டல் இரத்த அழுத்த மானி (BP Monitor)",
        "typeEn": "Cardiovascular Monitor",
        "typeTa": "இரத்த அழுத்த மானி",
        "doseEn": "Wrap cuff around bare upper arm at heart level while seated quietly for 5 mins.",
        "doseTa": "5 நிமிடம் அமைதியாக அமர்ந்த பின் இதய மட்டத்தில் கையில் கட்டவும்.",
        "limitEn": "Normal: <120/80 mmHg. High: >=140/90 mmHg.",
        "limitTa": "சாதாரண அளவு: <120/80. அதிகம்: >=140/90.",
        "cautionEn": "Detects silent hypertension and prevents sudden strokes in rural communities.",
        "cautionTa": "மாரடைப்பு மற்றும் பக்கவாதம் வராமல் தடுக்க இரத்த அழுத்தத்தை தினமும் கண்காணிக்கவும்."
    }
]

def get_medicines(category: str = "all", lang: str = "English") -> list[dict]:
    is_tamil = lang == "Tamil"
    items = []
    for m in ESSENTIAL_MEDS:
        if category != "all" and m["category"] != category:
            continue
        items.append({
            "id": m["id"],
            "category": m["category"],
            "icon": m["icon"],
            "name": m["nameTa"] if is_tamil else m["nameEn"],
            "type": m["typeTa"] if is_tamil else m["typeEn"],
            "dose": m["doseTa"] if is_tamil else m["doseEn"],
            "limit": m["limitTa"] if is_tamil else m["limitEn"],
            "caution": m["cautionTa"] if is_tamil else m["cautionEn"],
        })
    return items
