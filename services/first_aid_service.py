# services/first_aid_service.py
"""
Offline First-Aid Protocols Service
Contains verified step-by-step first-aid protocols in English and Tamil.
Can be rendered server-side via Jinja2 and accessed 100% offline.
"""

WOUND_PROTOCOLS = {
    "severe-bleeding": {
        "en": {
            "title": "🚨 Severe & Arterial Bleeding Control",
            "severity": "Life-Threatening Emergency Protocol",
            "severityClass": "status-urgent",
            "step1": "Direct Continuous Palm Pressure: Place thick sterile gauze or clean cloth directly on the wound. Press down with full body weight for 10-15 minutes continuously without lifting.",
            "step2": "Limb Elevation: If on arm or leg, immediately raise it above heart level to reduce arterial perfusion pressure.",
            "step3": "Pressure Bandage: Wrap elastic or roller bandage tightly over the dressing.",
            "step4": "Emergency Improvised Tourniquet: If limb bleed spurts and cannot be stopped, tie a wide cloth 2-3 inches above the wound. Tighten with a stick until bleeding stops. Record exact time.",
            "donts": [
                "Do NOT remove soaked bottom cloth; stack clean cloths on top.",
                "Do NOT use narrow wire or string as tourniquet.",
                "Do NOT loosen tourniquet once applied."
            ],
            "transport": "Mandatory Emergency Transport: Call 108 or arrange a vehicle immediately. Severe blood loss causes hypovolemic shock within minutes."
        },
        "ta": {
            "title": "🚨 தீவிர இரத்தப்போக்கு & டூர்னிகெட் நெறிமுறை",
            "severity": "உடனடி உயிர்காக்கும் அவசர சிகிச்சை",
            "severityClass": "status-urgent",
            "step1": "நேரடி அழுத்தம்: சுத்தமான தடிமனான துணி அல்லது காஸ் வைத்து உள்ளங்கையால் முழு பலத்துடன் 10-15 நிமிடங்கள் விடாமல் அழுத்திப் பிடிக்கவும்.",
            "step2": "உயர்த்தி வைத்தல்: காயம் கை அல்லது காலில் இருந்தால், அதை இதய மட்டத்திற்கு மேல் உயர்த்தி வைக்கவும்.",
            "step3": "அழுத்தக்கட்டு: இரத்தப்போக்கு நின்றதும் ரோலர் பேண்டேஜ் மூலம் உறுதியாக கட்டவும்.",
            "step4": "டூர்னிகெட் (கை/கால் தீவிர இரத்தப்போக்கிற்கு மட்டும்): இரத்தம் பீறிட்டால், காயத்திற்கு 2-3 அங்குலம் மேலே அகலமான துணியால் இறுகக் கட்டி நேரம் குறித்துக் கொள்ளவும்.",
            "donts": [
                "இரத்தம் நனைந்த துணியை எடுக்கக் கூடாது; அதன் மேல் புதிய துணியை வைக்கவும்.",
                "கம்பி அல்லது மெல்லிய கயிறு பயன்படுத்தக் கூடாது.",
                "ஒருமுறை கட்டிய பின் டூர்னிகெட்டை தளர்த்தக் கூடாது."
            ],
            "transport": "மருத்துவமனை செல்வது கட்டாயம்: 108 அழைக்கவும் அல்லது உடனடியாக வாகனத்தில் ஆரம்ப சுகாதார நிலையத்திற்கு (PHC) கொண்டு செல்லவும்."
        }
    },
    "minor-cuts": {
        "en": {
            "title": "🩹 Minor Cuts, Scrapes & Bleeding",
            "severity": "Mild - Home First-Aid",
            "severityClass": "status-good",
            "step1": "Cleanse with Water: Flush under running tap water for 5 minutes with mild soap around edges to wash away sand and dirt.",
            "step2": "Gentle Pressure: Pat dry with sterile gauze and apply light pressure to stop oozing.",
            "step3": "Antiseptic Application: Apply Povidone-Iodine 5% (Betadine) or Neosporin ointment.",
            "step4": "Sterile Bandage: Cover with a clean adhesive bandage. Change dressing daily or if wet.",
            "donts": [
                "Do NOT blow on the wound with your mouth (introduces oral bacteria).",
                "Do NOT use harsh alcohol or hydrogen peroxide directly inside fresh cuts."
            ],
            "transport": "Visit Doctor: If cut edges gape open (needs stitches) or red streaks appear after 2 days."
        },
        "ta": {
            "title": "🩹 சிறிய வெட்டுக்காயம், சிராய்ப்பு & இரத்தக் கசிவு",
            "severity": "லேசானது - வீட்டு முதலுதவி",
            "severityClass": "status-good",
            "step1": "சுத்தமான நீர்: ஓடும் குழாய் நீரில் 5 நிமிடங்கள் கழுவி மண், அழுக்கை அகற்றவும்.",
            "step2": "மென்மையான அழுத்தம்: சுத்தமான துணியால் ஒற்றி எடுத்து இரத்தம் கசிவதை நிறுத்தவும்.",
            "step3": "கிருமிநாசினி: Betadine அல்லது Neosporin களிம்பை காயத்தின் மேல் தடவவும்.",
            "step4": "பேண்டேஜ்: மலட்டு துணி அல்லது பேண்ட்-எய்ட் போடவும். தினமும் ஒரு முறை மாற்றவும்.",
            "donts": [
                "வாயால் காயத்தில் ஊதக் கூடாது (வாய் பாக்டீரியா பரவும்).",
                "ஹைட்ரஜன் பெராக்சைடு போட்டு காயத்தை எரிக்க வேண்டாம்."
            ],
            "transport": "மருத்துவரை அணுகவும்: காயம் ஆழமாக இருந்து சதைகள் பிரிந்திருந்தால் அல்லது 2 நாட்களுக்குப் பின் சீழ் பிடித்தால்."
        }
    },
    "burns": {
        "en": {
            "title": "🔥 Thermal Burns (1st to 3rd Degree)",
            "severity": "Urgent Thermal Care Protocol",
            "severityClass": "status-urgent",
            "step1": "20-Minute Cool Running Water: Place burnt area immediately under room-temperature flowing tap water for 20 full minutes. Never use ice or ice water.",
            "step2": "Remove Constrictions: Gently take off rings, watches, belts, or tight clothing before swelling sets in.",
            "step3": "Topical Burn Cream: Apply Silver Sulfadiazine 1% (Burnol) or sterile petroleum jelly.",
            "step4": "Cover Loosely: Drape with clean, non-stick sterile gauze or plastic food cling film.",
            "donts": [
                "NEVER apply toothpaste, butter, raw egg, turmeric, or cow dung.",
                "NEVER pop or peel fluid-filled blisters."
            ],
            "transport": "Hospitalization Required: If burn is larger than the victim's palm, on face/groin/joints, or caused by chemicals/electricity."
        },
        "ta": {
            "title": "🔥 தீக்காயங்கள் (1st முதல் 3rd Degree முதலுதவி)",
            "severity": "தீவிர கவனிப்பு தேவை",
            "severityClass": "status-urgent",
            "step1": "20 நிமிடம் குளிர்ந்த நீர்: சாதாரண ஓடும் குழாய் நீரில் 20 நிமிடங்கள் தொடர்ந்து வைக்கவும். ஐஸ் கட்டி வைக்கக் கூடாது.",
            "step2": "ஆடைகளை தளர்த்துதல்: மோதிரம், வளையல், கடிகாரத்தை வீங்குவதற்குள் மெதுவாக கழற்றவும்.",
            "step3": "மருந்து பூசுதல்: Silver Sulfadiazine 1% (சில்வர் சல்படயாசின்) கிரீம் தடவவும்.",
            "step4": "லேசாக மூடுதல்: சுத்தமான ஒட்டாத துணியால் லேசாக மூடவும்.",
            "donts": [
                "பற்பசை, வெண்ணெய், எண்ணெய் எதையும் பூசக்கூடாது.",
                "கொப்புளங்களை உடைக்கக் கூடாது."
            ],
            "transport": "மருத்துவமனை செல்வது அவசியம்: காயம் உள்ளங்கையை விட பெரிதாக இருந்தால் அல்லது முகம், மூட்டுகளில் பட்டிருந்தால்."
        }
    },
    "fractures": {
        "en": {
            "title": "🦴 Fractures & Severe Sprains",
            "severity": "Immobilization & Splint Protocol",
            "severityClass": "status-moderate",
            "step1": "Do NOT Realign: Never attempt to snap, twist, or force broken bone back into place.",
            "step2": "Improvised Splint: Use rolled newspapers, stiff cardboard, or wooden sticks padded with cloth alongside the limb.",
            "step3": "Secure Gently: Tie with cloth strips above and below the injury, not directly on the fracture site.",
            "step4": "RICE for Sprains: Rest, Ice pack wrapped in towel (20 min), Compression bandage, Elevation.",
            "donts": [
                "Do NOT massage violently with hot balm.",
                "Do NOT test if you can walk on a broken foot."
            ],
            "transport": "X-Ray & Orthopedic Care: Transport safely keeping the splinted limb completely still."
        },
        "ta": {
            "title": "🦴 எலும்பு முறிவு மற்றும் தசை சுளுக்கு",
            "severity": "அசைக்காமல் வைத்தல்",
            "severityClass": "status-moderate",
            "step1": "எலும்பை இழுக்காதீர்கள்: உடைந்த எலும்பை நீங்களாக சரிசெய்யவோ திருப்பவோ கூடாது.",
            "step2": "அவசர ஸ்பிளின்ட்: தடிமனான அட்டை அல்லது குச்சியை துணியில் சுற்றி கை/காலின் இருபுறமும் வைக்கவும்.",
            "step3": "கட்டுதல்: முறிவு ஏற்பட்ட இடத்திற்கு மேலும் கீழும் துணியால் மென்மையாக கட்டவும்.",
            "step4": "சுளுக்குக்கு: ஓய்வு, துணியில் சுற்றிய ஐஸ் ஒத்தடம், லேசான கட்டு, உயர்த்தி வைத்தல்.",
            "donts": [
                "சூடான தைலம் தடவி வேகமாக தேய்க்கக் கூடாது.",
                "எலும்பு உடைந்த காலில் நடக்க முயற்சிக்க வேண்டாம்."
            ],
            "transport": "மருத்துவமனைக்கு: பாதுகாப்பாக நோயாளியை படுக்க வைத்து எக்ஸ்ரே எடுக்க மருத்துவமனைக்கு அழைத்துச் செல்லவும்."
        }
    },
    "snakebites": {
        "en": {
            "title": "🐍 Venomous Snakebites (Anti-Venom Protocol)",
            "severity": "Life-Threatening Emergency - Immediate Action",
            "severityClass": "status-urgent",
            "step1": "Complete Immobility & Calming: Reassure the victim. Keep them 100% physically still. Any movement or panic pumps venom through the lymphatic system faster.",
            "step2": "Immobilize the Limb at or Below Heart Level: Use a flat wooden board, cardboard, or bamboo splint to immobilize the bitten arm/leg just like a fracture. Gently bandage without cutting off pulse.",
            "step3": "Remove Constricting Items: Immediately slip off rings, bangles, anklets, or tight shoes before swelling begins.",
            "step4": "Rush to Hospital with Anti-Snake Venom (ASV): Transport in a vehicle or lying down. Alert Primary Health Center (PHC) or district hospital.",
            "donts": [
                "NEVER cut the bite with blades or knives.",
                "NEVER attempt to suck venom by mouth or pump.",
                "NEVER tie a tight rope or arterial tourniquet (causes tissue necrosis/gangrene).",
                "NEVER give aspirin, painkiller injections, or alcohol."
            ],
            "transport": "Hospital ASV is the ONLY antidote: Time is vital. Reach a hospital with polyvalent Anti-Snake Venom within 1-2 hours. Note snake appearance if safely visible, but NEVER attempt to catch or kill it."
        },
        "ta": {
            "title": "🐍 பாம்பு கடி அவசர முதலுதவி (உயிர்காக்கும் ASV நெறிமுறை)",
            "severity": "உடனடி அவசர மருத்துவமனை சிகிச்சை",
            "severityClass": "status-urgent",
            "step1": "முழுமையான அசைவின்மை: பாதிக்கப்பட்டவரை முற்றிலும் அமைதிப்படுத்தி, துளியும் நடக்கவோ அசையவோ விடாமல் படுக்க வைக்கவும். பதற்றமும் அசைவும் விஷத்தை உடல் முழுவதும் வேகமாகப் பரப்பும்.",
            "step2": "கடித்த இடத்தை நிலைநிறுத்துதல்: கடித்த கையை அல்லது காலை இதய மட்டத்திற்கு கீழே வைத்து, மரக்கட்டை அல்லது தடிமனான அட்டை வைத்து அசைக்க முடியாமல் மென்மையாகக் கட்டவும் (இரத்த ஓட்டம் தடைபடக் கூடாது).",
            "step3": "ஆடைகள்/ஆபரணங்களை அகற்றுதல்: வீக்கம் வருவதற்குள் மோதிரம், கொலுசு, காலணிகள், இறுக்கமான ஆடைகளை உடனடியாக கழற்றவும்.",
            "step4": "உடனடி மருத்துவமனை பயணம்: நோயாளியை படுக்க வைத்தவாறே 108 அவசர ஊர்தி அல்லது வாகனத்தில் Anti-Snake Venom (ASV) மருந்துள்ள அரசு மருத்துவமனைக்குக் கொண்டு செல்லவும்.",
            "donts": [
                "பிளேடு அல்லது கத்தியால் காயத்தை கீறக் கூடாது.",
                "வாயால் விஷத்தை உறிஞ்ச முயற்சிக்கவே கூடாது.",
                "கயிறு கொண்டு மிக இறுக்கமாக ரத்த ஓட்டத்தை நிறுத்தக் கட்டக் கூடாது (இது தசையை அழுகச் செய்யும்).",
                "ஆஸ்பிரின், வலி நிவாரணிகள் அல்லது நாட்டு மருந்துகளை தரக் கூடாது."
            ],
            "transport": "ASV மட்டுமே விஷ முறிவு மருந்து: பாம்பு கடித்த 1-2 மணி நேரத்திற்குள் அரசு மருத்துவமனைக்குச் செல்ல வேண்டும். பாம்பை பிடிக்கவோ அடிக்கவோ முயன்று நேரத்தை வீணடிக்காதீர்கள்."
        }
    },
    "animal-bites": {
        "en": {
            "title": "🐕 Dog, Cat & Animal Bites (Rabies Prevention)",
            "severity": "Urgent Fatal Risk Without Vaccine",
            "severityClass": "status-urgent",
            "step1": "15-Minute Continuous Soap & Running Water Flush: Immediately place the bite under flowing tap water with laundry/toilet soap for a full 15 minutes. Soap dissolves the lipid envelope of rabies virus and eliminates >70% of viral load.",
            "step2": "Disinfect Wound Surface: Apply Povidone-Iodine 5% (Betadine) or 70% alcohol generously. Avoid covering tightly.",
            "step3": "Urgent Anti-Rabies Vaccine (ARV): Must receive Day-0 ARV dose at government clinic/hospital within 24 hours.",
            "step4": "Rabies Immunoglobulin (RIG): Category III bites (broken skin or bleeding) require RIG infiltrated around the wound on Day 0.",
            "donts": [
                "Do NOT apply chili powder, turmeric, lime, or cow dung.",
                "Do NOT bandage tightly or suture/stitch fresh bite wounds.",
                "Do NOT delay vaccine assuming pet was vaccinated unless vet confirms."
            ],
            "transport": "Government Hospital ARV Protocol: Day 0, Day 3, Day 7, Day 14, and Day 28 doses are mandatory. Rabies is 100% fatal once symptoms appear, but 100% preventable with prompt vaccination."
        },
        "ta": {
            "title": "🐕 நாய் மற்றும் விலங்கு கடி (ரேபிஸ் தடுப்பு முதலுதவி)",
            "severity": "தடுப்பூசி இல்லையெனில் உயிருக்கு ஆபத்து",
            "severityClass": "status-urgent",
            "step1": "15 நிமிடம் சோப்பு போட்டு கழுவுதல்: கடிபட்ட இடத்தை உடனடியாக ஓடும் குழாய் நீரில் சோப்பு போட்டு முழுமையாக 15 நிமிடங்கள் இடைவிடாமல் கழுவவும். சோப்பு நுரை ரேபிஸ் வைரஸின் 70% மேல் அழித்துவிடும்.",
            "step2": "கிருமிநாசினி பூசுதல்: Betadine அல்லது 70% ஆல்கஹால் திரவத்தை காயத்தின் மேல் தாராளமாக ஊற்றி சுத்தம் செய்யவும். காற்று புகாமல் அடைக்க வேண்டாம்.",
            "step3": "ரேபிஸ் தடுப்பூசி (ARV): 24 மணி நேரத்திற்குள் ஆரம்ப சுகாதார நிலையம் அல்லது அரசு மருத்துவமனையில் Day-0 ரேபிஸ் தடுப்பூசி போட வேண்டும்.",
            "step4": "இம்யூனோகுளோபுலின் (RIG): இரத்தம் வரும் ஆழமான கடிக்கு (Category III) காயத்தைச் சுற்றி போடும் RIG மருந்து அவசியம்.",
            "donts": [
                "மிளகாய் பொடி, சுண்ணாம்பு, சாணம், எண்ணெய் எதையும் காயத்தில் வைக்கக் கூடாது.",
                "காயத்தை உடனே தைக்கவோ அல்லது இறுக்கமாக பிளாஸ்திரி போடவோ கூடாது.",
                "வீட்டு நாய் தானே என்று தடுப்பூசி போடுவதை தாமதிக்கக் கூடாது."
            ],
            "transport": "அரசு மருத்துவமனையில் இலவச தடுப்பூசி: Day 0, 3, 7, 14, 28 அட்டவணைப்படி முழுமையாக தடுப்பூசி போடவும். ரேபிஸ் அறிகுறிகள் தோன்றினால் குணப்படுத்த முடியாது, ஆனால் தடுப்பூசி போட்டால் 100% தடுக்க முடியும்."
        }
    },
    "unconsciousness": {
        "en": {
            "title": "🫀 Unconsciousness, Fainting & CPR (DRSABCD Protocol)",
            "severity": "Life-Threatening Emergency - Immediate Resuscitation",
            "severityClass": "status-urgent",
            "step1": "DRS Check (Danger, Response, Send for Help): Ensure area is safe. Tap shoulders and shout: 'Are you okay?'. If unresponsive, shout for help and immediately call 108.",
            "step2": "Airway & Breathing Check: Gently tilt head back and lift chin. Look, listen, and feel for normal breathing for 10 seconds (agonal gasping is NOT normal breathing).",
            "step3": "If Breathing Normally -> Recovery Position: Roll victim onto their side. Bend top knee to prop them up. Tilt head gently back to keep airway open and prevent choking on saliva or vomit.",
            "step4": "If NOT Breathing -> Start CPR Immediately: Place heel of palm on center of chest. Interlock other hand. Push hard and fast (100-120 compressions/min, 2 inches deep). Give 30 compressions followed by 2 rescue breaths (or continuous Hands-Only CPR without stopping) until ambulance arrives.",
            "donts": [
                "NEVER give water, food, or medicines to an unconscious person (causes fatal aspiration choking).",
                "NEVER shake a person with suspected head or neck injury.",
                "NEVER crowd around victim; ensure maximum fresh airflow.",
                "Do NOT stop CPR until medical help takes over or victim moves."
            ],
            "transport": "Immediate 108 Emergency Transport: Unconsciousness indicates cardiac arrest, stroke, severe head trauma, or respiratory failure. Continuous CPR maintains oxygen to the brain until defibrillator/paramedics arrive."
        },
        "ta": {
            "title": "🫀 சுயநினைவின்மை, மயக்கம் & CPR முதலுதவி (DRSABCD நெறிமுறை)",
            "severity": "உடனடி உயிர்காக்கும் அவசர சிகிச்சை",
            "severityClass": "status-urgent",
            "step1": "சோதித்தல் & 108 அழைப்பு: பாதுகாப்பான இடமா எனப் பார்த்து, தோள்களைத் தட்டி 'நீங்கள் நலமாக உள்ளீர்களா?' எனக் குரல் எழுப்பவும். பதிலில்லை எனில் உடனே சுற்றியுள்ளவர்களை உதவிக்கு அழைத்து 108 அழைக்கச் சொல்லவும்.",
            "step2": "சுவாசப் பரிசோதனை: தலையை மெதுவாக பின்நோக்கி சாய்த்து, தாடையை உயர்த்தவும். மார்பு ஏறி இறங்குகிறதா, மூச்சுக்காற்று வருகிறதா என 10 வினாடிகள் கவனிக்கவும்.",
            "step3": "சுவாசம் இருந்தால் -> பக்கவாட்டு மீட்பு நிலை (Recovery Position): நோயாளியை பக்கவாட்டில் ஒருபுறமாக திருப்பி, தலையை லேசாக உயர்த்தி வைக்கவும். இது நாக்கு தொண்டையை அடைக்காமல், வாந்தி எடுத்தாலும் மூச்சுக்குழாய்க்குள் செல்லாமல் காக்கும்.",
            "step4": "சுவாசம் இல்லையெனில் -> உடனடியாக CPR தொடங்கவும்: மார்பின் நடுப்பகுதியில் உள்ளங்கையை வைத்து, மற்றொரு கையை கோர்த்துக்கொள்ளவும். நிமிடத்திற்கு 100-120 முறை வேகமாகவும், 2 அங்குல ஆழத்திலும் இடைவிடாமல் அழுத்தவும் (30 அழுத்தங்கள் : 2 செயற்கை சுவாசம், அல்லது தொடர்ந்து மார்பு அழுத்தம் மட்டும்) ஆம்புலன்ஸ் வரும் வரை நிறுத்த வேண்டாம்.",
            "donts": [
                "மயக்கமடைந்தவருக்கு ஒருபோதும் தண்ணீர் அல்லது மருந்து புகட்டக் கூடாது (மூச்சுக்குழாயில் அடைத்து மரணம் ஏற்படும்).",
                "தலையில் அடிபட்டவரை வேகமாக குலுக்கவோ அசைக்கவோ கூடாது.",
                "நோயாளியைச் சுற்றி கூட்டம் கூடாமல் நல்ல காற்று வர அனுமதிக்கவும்.",
                "ஆம்புலன்ஸ் வரும் வரை CPR செய்வதை நிறுத்தக் கூடாது."
            ],
            "transport": "உடனடி 108 அவசர ஊர்தி: சுயநினைவின்மை மாரடைப்பு, பக்கவாதம் அல்லது மூளை பாதிப்பின் அறிகுறி. CPR செய்வதன் மூலம் மூளைக்கு ஆக்சிஜன் செல்வதை உறுதி செய்து உயிரைக் காப்பாற்ற முடியும்."
        }
    },
    "puncture-wounds": {
        "en": {
            "title": "🔩 Puncture Wounds & Rusty Nails (Tetanus)",
            "severity": "High Tetanus Risk Protocol",
            "severityClass": "status-moderate",
            "step1": "Mechanical Wash: Run under flowing tap water with soap for a full 5-10 minutes to clear anaerobic bacteria.",
            "step2": "Do NOT Squeeze Hard: Avoid deep digging or probing with needles.",
            "step3": "Disinfect: Apply generous Betadine liquid to the puncture entrance.",
            "step4": "Tetanus Toxoid (TT) Injection: Essential within 24 hours if last TT shot was >5 years ago.",
            "donts": [
                "Do NOT seal completely airtight with duct tape.",
                "Do NOT leave rusty particles inside."
            ],
            "transport": "Urgent Clinic Visit: Mandatory for Tetanus injection and antibiotic evaluation."
        },
        "ta": {
            "title": "🔩 ஆணி / முள் குத்திய ஆழமான காயங்கள் (டெட்டனஸ்)",
            "severity": "டெட்டனஸ் ஆபத்து",
            "severityClass": "status-moderate",
            "step1": "ஓடும் நீரில் கழுவுதல்: சோப்பு போட்டு 5-10 நிமிடங்கள் அழுக்கு வெளியேறும் வரை கழுவவும்.",
            "step2": "ஆழமாக குத்தாதீர்கள்: ஊசி அல்லது பிளேடால் காயத்தை கிளற வேண்டாம்.",
            "step3": "கிருமிநாசினி: Betadine திரவத்தை காயத்தின் மீது ஊற்றி சுத்தம் செய்யவும்.",
            "step4": "TT தடுப்பூசி: 24 மணி நேரத்திற்குள் டெட்டனஸ் டாக்சாய்டு (TT) ஊசி போடுவது மிக அவசியம்.",
            "donts": [
                "காற்று புகாதவாறு பிளாஸ்திரி கொண்டு அடைக்கக் கூடாது.",
                "துருத்துண்டுகள் உள்ளே இருந்தால் சொந்தமாக எடுக்க முயற்சிக்காதீர்கள்."
            ],
            "transport": "மருத்துவமனை செல்வது கட்டாயம்: TT தடுப்பூசி மற்றும் தொற்று தடுப்பு மருந்துக்கு உடனே செல்லவும்."
        }
    },
    "sepsis": {
        "en": {
            "title": "⚠️ Sepsis & Severe Wound Infection",
            "severity": "Life-Threatening Systemic Infection",
            "severityClass": "status-urgent",
            "step1": "Recognize Red Streaks: Red lines radiating from the wound towards the heart indicates lymphangitis/bloodstream infection.",
            "step2": "Foul Odor & Throbbing Pus: Thick yellowish-green discharge and burning local heat.",
            "step3": "Systemic Signs: High fever (>101°F), shaking chills, rapid heart rate (>100 bpm), confusion, extreme weakness.",
            "step4": "Immediate Hospital Care: Sepsis requires IV antibiotics and surgical wound drainage.",
            "donts": [
                "Do NOT squeeze or burst infected abscesses with dirty pins.",
                "Do NOT rely solely on home herbs when systemic fever starts."
            ],
            "transport": "Non-Negotiable ER Transport: Sepsis is an extreme medical emergency. Call 108 or arrange urgent car transport."
        },
        "ta": {
            "title": "⚠️ சீழ் தொற்று மற்றும் செப்சிஸ் (இரத்த நச்சு)",
            "severity": "உயிருக்கு ஆபத்தான தீவிர தொற்று",
            "severityClass": "status-urgent",
            "step1": "சிவந்த கோடுகள்: காயத்திலிருந்து இதயத்தை நோக்கி சிவந்த கோடுகள் பரவினால் தொற்று இரத்தத்தில் கலக்கிறது என்று பொருள்.",
            "step2": "சீழ் & துர்நாற்றம்: காயத்திலிருந்து துர்நாற்றத்துடன் கூடிய மஞ்சள்-பச்சை சீழ் வெளியேறுதல்.",
            "step3": "உடல் முழுவதும் தாக்கம்: கடுமையான காய்ச்சல் (101°F மேல்), நடுக்கம், வேகமான இதயத் துடிப்பு, குழப்பம், அதீத சோர்வு.",
            "step4": "உடனடி சிகிச்சை: இதற்கு நரம்பு வழி ஆன்டிபயாடிக் (IV Antibiotics) சிகிச்சை மருத்துவமனையில் மட்டுமே தர முடியும்.",
            "donts": [
                "சீழ் கட்டியை அழுத்தி உடைக்கக் கூடாது.",
                "காய்ச்சல் வந்த பிறகு நாட்டு மருந்துகளுடன் நேரத்தை கடத்தக் கூடாது."
            ],
            "transport": "உடனடி மருத்துவமனை: தாமதிக்காமல் 108 அவசர ஊர்தி அல்லது வாகனத்தில் அவசர சிகிச்சைப் பிரிவுக்குச் செல்லவும்."
        }
    }
}

def get_wound_protocol(wound_key: str, lang: str = "English") -> dict:
    key = wound_key if wound_key in WOUND_PROTOCOLS else "severe-bleeding"
    lang_code = "ta" if lang == "Tamil" else "en"
    return WOUND_PROTOCOLS[key][lang_code]

def get_all_wound_keys() -> list[str]:
    return list(WOUND_PROTOCOLS.keys())
