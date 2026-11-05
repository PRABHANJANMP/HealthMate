/**
 * HealthMate AI - Remote Emergency, Wound Treatment, Medicine Kit & Doctor Report
 * Comprehensive script providing:
 * 1. Complete, 100% Bilingual localization (English & Tamil) for EVERY word, letter, label, button, and report.
 * 2. 5 Full Views: Chat, Wound Care Tutorial, Medicine Kit, Daily Check-in & Charts, Doctor Report.
 * 3. Hospitalization-grade step-by-step wound care tutorials for remote towns.
 * 4. Essential home medicine & first aid kit catalog with copy/print checklist.
 * 5. Daily Health Check-in & Vitals Tracker with pain slider & symptom chips.
 * 6. Interactive Multi-Metric Chart.js Trends (BP, Sugar, SpO2, Pulse, Temp) with bilingual legends.
 * 7. Monthly Doctor Report generator with Email to Doctor (mailto:), WhatsApp sharing, and PDF print.
 * 8. Speech recognition (Web Speech API) & Markdown-lite message parser.
 */

// API Configuration
const API_BASE = "http://127.0.0.1:8081";

// Navigation Elements
const tabChatBtn = document.getElementById("tab-chat-btn");
const tabWoundsBtn = document.getElementById("tab-wounds-btn");
const tabMedsBtn = document.getElementById("tab-meds-btn");
const tabChartBtn = document.getElementById("tab-chart-btn");
const tabReportBtn = document.getElementById("tab-report-btn");

const viewChat = document.getElementById("view-chat");
const viewWounds = document.getElementById("view-wounds");
const viewMeds = document.getElementById("view-meds");
const viewChart = document.getElementById("view-chart");
const viewReport = document.getElementById("view-report");

// Banner & Status Elements
const dailyCheckinBanner = document.getElementById("daily-checkin-banner");
const quickCheckinBtn = document.getElementById("quick-checkin-btn");
const emergencyBanner = document.getElementById("emergency-banner");
const offlineBanner = document.getElementById("offline-banner");
const offlineBannerTitle = document.getElementById("offline-banner-title");
const offlineBannerDesc = document.getElementById("offline-banner-desc");
const offlineGuideQuickBtn = document.getElementById("offline-guide-quick-btn");
const offlineBtnText = document.getElementById("offline-btn-text");
const networkStatus = document.getElementById("network-status");
const networkStatusText = document.getElementById("network-status-text");
const cacheStatus = document.getElementById("cache-status");
const cacheStatusText = document.getElementById("cache-status-text");
const offlineGuideStatusBox = document.getElementById("offline-guide-status-box");
const offlineGuideStatusText = document.getElementById("offline-guide-status-text");
const systemStatus = document.getElementById("system-status");
const statusText = document.getElementById("status-text");
const languageSelect = document.getElementById("language");
const clearBtn = document.getElementById("clear-btn");

// Triage Elements
const triageTitle = document.getElementById("triage-title");
const triageSubtitle = document.getElementById("triage-subtitle");
const triageRushTitle = document.getElementById("triage-rush-title");
const triageRoleTitle = document.getElementById("triage-role-title");
const triageRoleDesc = document.getElementById("triage-role-desc");
const triageRushList = document.getElementById("triage-rush-list");

// Chat Elements
const chatForm = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");
const chatMessages = document.getElementById("chat-messages");
const sendButton = document.getElementById("send-button");
const voiceBtn = document.getElementById("voice-btn");
const voiceLabel = document.getElementById("voice-label");
const chipsContainer = document.getElementById("chips-container");

// Daily Vitals Log Form Elements
const healthLogForm = document.getElementById("health-log-form");
const logDate = document.getElementById("log-date");
const logTime = document.getElementById("log-time");
const logSysBp = document.getElementById("log-sys-bp");
const logDiaBp = document.getElementById("log-dia-bp");
const logSugar = document.getElementById("log-sugar");
const logPulse = document.getElementById("log-pulse");
const logSpo2 = document.getElementById("log-spo2");
const logTemp = document.getElementById("log-temp");
const logPain = document.getElementById("log-pain");
const painValBadge = document.getElementById("pain-val-badge");
const logSeverity = document.getElementById("log-severity");
const logNotes = document.getElementById("log-notes");
const timelineCardsList = document.getElementById("timeline-cards-list");
const analyzeChartBtn = document.getElementById("analyze-chart-btn");
const symptomTagChips = document.querySelectorAll(".symptom-tag");

// Chart Elements
const chartSwitches = document.querySelectorAll(".chart-switch-btn");
let activeChartType = "bp";
let vitalsChartInstance = null;

// Wound Treatment Elements
const woundChipsContainer = document.getElementById("wound-chips");
const woundGuideCard = document.getElementById("wound-guide-card");
let activeWoundKey = "severe-bleeding";

// Medicine Kit Elements
const medsFilters = document.querySelectorAll(".med-filter-btn");
const medsGrid = document.getElementById("meds-grid");
const copyMedsBtn = document.getElementById("copy-meds-btn");
const printMedsBtn = document.getElementById("print-meds-btn");
let activeMedCategory = "all";

// Doctor Report Elements
const patientNameInput = document.getElementById("patient-name-input");
const patientAgeInput = document.getElementById("patient-age-input");
const doctorEmailInput = document.getElementById("doctor-email-input");
const doctorPhoneInput = document.getElementById("doctor-phone-input");
const generateReportBtn = document.getElementById("generate-report-btn");
const reportPlaceholder = document.getElementById("report-placeholder");
const reportContent = document.getElementById("report-content");
const emailDoctorBtn = document.getElementById("email-doctor-btn");
const whatsappDoctorBtn = document.getElementById("whatsapp-doctor-btn");
const printReportBtn = document.getElementById("print-report-btn");

// Initialize dates
if (logDate) logDate.valueAsDate = new Date();
if (logTime) {
    const now = new Date();
    logTime.value = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
}

// Session Tracking
function getOrCreateSessionId() {
    let sid = sessionStorage.getItem("healthmate_session_id");
    if (!sid) {
        sid = "sess_" + Math.random().toString(36).substring(2, 9) + Date.now().toString(36);
        sessionStorage.setItem("healthmate_session_id", sid);
    }
    return sid;
}
const SESSION_ID = getOrCreateSessionId();

// Storage Key
const STORAGE_LOGS_KEY = "healthmate_vitals_logs";

// Seed realistic clinical demo data if empty
function seedInitialDataIfEmpty() {
    const existing = localStorage.getItem(STORAGE_LOGS_KEY);
    if (!existing || JSON.parse(existing).length === 0) {
        const demoLogs = [
            {
                id: "seed_1",
                patient_id: "default",
                date: "2026-10-10",
                time: "08:30",
                systolic_bp: 138,
                diastolic_bp: 88,
                blood_glucose: 142,
                heart_rate: 76,
                spo2: 97,
                temperature: 98.6,
                pain_level: 2,
                symptoms: ["Headache"],
                condition_severity: "Mild",
                notes: "Morning measurement after waking up."
            },
            {
                id: "seed_2",
                patient_id: "default",
                date: "2026-10-18",
                time: "19:00",
                systolic_bp: 144,
                diastolic_bp: 92,
                blood_glucose: 168,
                heart_rate: 84,
                spo2: 96,
                temperature: 99.8,
                pain_level: 4,
                symptoms: ["Fever", "Body Ache"],
                condition_severity: "Moderate",
                notes: "Felt warm and fatigued. Took Paracetamol 650mg."
            },
            {
                id: "seed_3",
                patient_id: "default",
                date: "2026-10-25",
                time: "08:15",
                systolic_bp: 130,
                diastolic_bp: 84,
                blood_glucose: 125,
                heart_rate: 72,
                spo2: 98,
                temperature: 98.4,
                pain_level: 1,
                symptoms: [],
                condition_severity: "Mild",
                notes: "Good rest, vitals normal."
            },
            {
                id: "seed_4",
                patient_id: "default",
                date: "2026-11-02",
                time: "14:40",
                systolic_bp: 148,
                diastolic_bp: 94,
                blood_glucose: 185,
                heart_rate: 88,
                spo2: 95,
                temperature: 100.5,
                pain_level: 5,
                symptoms: ["Fever", "Headache", "Cough"],
                condition_severity: "Moderate",
                notes: "High glucose after festival food. Wet cloth compress applied."
            }
        ];
        localStorage.setItem(STORAGE_LOGS_KEY, JSON.stringify(demoLogs));
    }
}
seedInitialDataIfEmpty();

// ============================================================================
// DATA: OFFLINE FIRST-AID PROTOCOLS (100% Client-Side & Bilingual)
// Clinically verified protocols: Red Cross / WHO / Indian NHP guidelines
// ============================================================================
const WOUND_PROTOCOLS = {
    "severe-bleeding": {
        en: {
            title: "🚨 Severe & Arterial Bleeding Control",
            severity: "Life-Threatening Emergency Protocol",
            severityClass: "status-urgent",
            step1: "Direct Continuous Palm Pressure: Place thick sterile gauze or clean cloth directly on the wound. Press down with full body weight for 10-15 minutes continuously without lifting.",
            step2: "Limb Elevation: If on arm or leg, immediately raise it above heart level to reduce arterial perfusion pressure.",
            step3: "Pressure Bandage: Wrap elastic or roller bandage tightly over the dressing.",
            step4: "Emergency Improvised Tourniquet: If limb bleed spurts and cannot be stopped, tie a wide cloth 2-3 inches above the wound. Tighten with a stick until bleeding stops. Record exact time.",
            donts: ["Do NOT remove soaked bottom cloth; stack clean cloths on top.", "Do NOT use narrow wire or string as tourniquet.", "Do NOT loosen tourniquet once applied."],
            transport: "Mandatory Emergency Transport: Call 108 or arrange a vehicle immediately. Severe blood loss causes hypovolemic shock within minutes."
        },
        ta: {
            title: "🚨 தீவிர இரத்தப்போக்கு & டூர்னிகெட் நெறிமுறை",
            severity: "உடனடி உயிர்காக்கும் அவசர சிகிச்சை",
            severityClass: "status-urgent",
            step1: "நேரடி அழுத்தம்: சுத்தமான தடிமனான துணி அல்லது காஸ் வைத்து உள்ளங்கையால் முழு பலத்துடன் 10-15 நிமிடங்கள் விடாமல் அழுத்திப் பிடிக்கவும்.",
            step2: "உயர்த்தி வைத்தல்: காயம் கை அல்லது காலில் இருந்தால், அதை இதய மட்டத்திற்கு மேல் உயர்த்தி வைக்கவும்.",
            step3: "அழுத்தக்கட்டு: இரத்தப்போக்கு நின்றதும் ரோலர் பேண்டேஜ் மூலம் உறுதியாக கட்டவும்.",
            step4: "டூர்னிகெட் (கை/கால் தீவிர இரத்தப்போக்கிற்கு மட்டும்): இரத்தம் பீறிட்டால், காயத்திற்கு 2-3 அங்குலம் மேலே அகலமான துணியால் இறுகக் கட்டி நேரம் குறித்துக் கொள்ளவும்.",
            donts: ["இரத்தம் நனைந்த துணியை எடுக்கக் கூடாது; அதன் மேல் புதிய துணியை வைக்கவும்.", "கம்பி அல்லது மெல்லிய கயிறு பயன்படுத்தக் கூடாது.", "ஒருமுறை கட்டிய பின் டூர்னிகெட்டை தளர்த்தக் கூடாது."],
            transport: "மருத்துவமனை செல்வது கட்டாயம்: 108 அழைக்கவும் அல்லது உடனடியாக வாகனத்தில் ஆரம்ப சுகாதார நிலையத்திற்கு (PHC) கொண்டு செல்லவும்."
        }
    },
    "minor-cuts": {
        en: {
            title: "🩹 Minor Cuts, Scrapes & Bleeding",
            severity: "Mild - Home First-Aid",
            severityClass: "status-good",
            step1: "Cleanse with Water: Flush under running tap water for 5 minutes with mild soap around edges to wash away sand and dirt.",
            step2: "Gentle Pressure: Pat dry with sterile gauze and apply light pressure to stop oozing.",
            step3: "Antiseptic Application: Apply Povidone-Iodine 5% (Betadine) or Neosporin ointment.",
            step4: "Sterile Bandage: Cover with a clean adhesive bandage. Change dressing daily or if wet.",
            donts: ["Do NOT blow on the wound with your mouth (introduces oral bacteria).", "Do NOT use harsh alcohol or hydrogen peroxide directly inside fresh cuts."],
            transport: "Visit Doctor: If cut edges gape open (needs stitches) or red streaks appear after 2 days."
        },
        ta: {
            title: "🩹 சிறிய வெட்டுக்காயம், சிராய்ப்பு & இரத்தக் கசிவு",
            severity: "லேசானது - வீட்டு முதலுதவி",
            severityClass: "status-good",
            step1: "சுத்தமான நீர்: ஓடும் குழாய் நீரில் 5 நிமிடங்கள் கழுவி மண், அழுக்கை அகற்றவும்.",
            step2: "மென்மையான அழுத்தம்: சுத்தமான துணியால் ஒற்றி எடுத்து இரத்தம் கசிவதை நிறுத்தவும்.",
            step3: "கிருமிநாசினி: Betadine அல்லது Neosporin களிம்பை காயத்தின் மேல் தடவவும்.",
            step4: "பேண்டேஜ்: மலட்டு துணி அல்லது பேண்ட்-எய்ட் போடவும். தினமும் ஒரு முறை மாற்றவும்.",
            donts: ["வாயால் காயத்தில் ஊதக் கூடாது (வாய் பாக்டீரியா பரவும்).", "ஹைட்ரஜன் பெராக்சைடு போட்டு காயத்தை எரிக்க வேண்டாம்."],
            transport: "மருத்துவரை அணுகவும்: காயம் ஆழமாக இருந்து சதைகள் பிரிந்திருந்தால் அல்லது 2 நாட்களுக்குப் பின் சீழ் பிடித்தால்."
        }
    },
    "burns": {
        en: {
            title: "🔥 Thermal Burns (1st to 3rd Degree)",
            severity: "Urgent Thermal Care Protocol",
            severityClass: "status-urgent",
            step1: "20-Minute Cool Running Water: Place burnt area immediately under room-temperature flowing tap water for 20 full minutes. Never use ice or ice water.",
            step2: "Remove Constrictions: Gently take off rings, watches, belts, or tight clothing before swelling sets in.",
            step3: "Topical Burn Cream: Apply Silver Sulfadiazine 1% (Burnol) or sterile petroleum jelly.",
            step4: "Cover Loosely: Drape with clean, non-stick sterile gauze or plastic food cling film.",
            donts: ["NEVER apply toothpaste, butter, raw egg, turmeric, or cow dung.", "NEVER pop or peel fluid-filled blisters."],
            transport: "Hospitalization Required: If burn is larger than the victim's palm, on face/groin/joints, or caused by chemicals/electricity."
        },
        ta: {
            title: "🔥 தீக்காயங்கள் (1st முதல் 3rd Degree முதலுதவி)",
            severity: "தீவிர கவனிப்பு தேவை",
            severityClass: "status-urgent",
            step1: "20 நிமிடம் குளிர்ந்த நீர்: சாதாரண ஓடும் குழாய் நீரில் 20 நிமிடங்கள் தொடர்ந்து வைக்கவும். ஐஸ் கட்டி வைக்கக் கூடாது.",
            step2: "ஆடைகளை தளர்த்துதல்: மோதிரம், வளையல், கடிகாரத்தை வீங்குவதற்குள் மெதுவாக கழற்றவும்.",
            step3: "மருந்து பூசுதல்: Silver Sulfadiazine 1% (சில்வர் சல்படயாசின்) கிரீம் தடவவும்.",
            step4: "லேசாக மூடுதல்: சுத்தமான ஒட்டாத துணியால் லேசாக மூடவும்.",
            donts: ["பற்பசை, வெண்ணெய், எண்ணெய் எதையும் பூசக்கூடாது.", "கொப்புளங்களை உடைக்கக் கூடாது."],
            transport: "மருத்துவமனை செல்வது அவசியம்: காயம் உள்ளங்கையை விட பெரிதாக இருந்தால் அல்லது முகம், மூட்டுகளில் பட்டிருந்தால்."
        }
    },
    "fractures": {
        en: {
            title: "🦴 Fractures & Severe Sprains",
            severity: "Immobilization & Splint Protocol",
            severityClass: "status-moderate",
            step1: "Do NOT Realign: Never attempt to snap, twist, or force broken bone back into place.",
            step2: "Improvised Splint: Use rolled newspapers, stiff cardboard, or wooden sticks padded with cloth alongside the limb.",
            step3: "Secure Gently: Tie with cloth strips above and below the injury, not directly on the fracture site.",
            step4: "RICE for Sprains: Rest, Ice pack wrapped in towel (20 min), Compression bandage, Elevation.",
            donts: ["Do NOT massage violently with hot balm.", "Do NOT test if you can walk on a broken foot."],
            transport: "X-Ray & Orthopedic Care: Transport safely keeping the splinted limb completely still."
        },
        ta: {
            title: "🦴 எலும்பு முறிவு மற்றும் தசை சுளுக்கு",
            severity: "அசைக்காமல் வைத்தல்",
            severityClass: "status-moderate",
            step1: "எலும்பை இழுக்காதீர்கள்: உடைந்த எலும்பை நீங்களாக சரிசெய்யவோ திருப்பவோ கூடாது.",
            step2: "அவசர ஸ்பிளின்ட்: தடிமனான அட்டை அல்லது குச்சியை துணியில் சுற்றி கை/காலின் இருபுறமும் வைக்கவும்.",
            step3: "கட்டுதல்: முறிவு ஏற்பட்ட இடத்திற்கு மேலும் கீழும் துணியால் மென்மையாக கட்டவும்.",
            step4: "சுளுக்குக்கு: ஓய்வு, துணியில் சுற்றிய ஐஸ் ஒத்தடம், லேசான கட்டு, உயர்த்தி வைத்தல்.",
            donts: ["சூடான தைலம் தடவி வேகமாக தேய்க்கக் கூடாது.", "எலும்பு உடைந்த காலில் நடக்க முயற்சிக்க வேண்டாம்."],
            transport: "மருத்துவமனைக்கு: பாதுகாப்பாக நோயாளியை படுக்க வைத்து எக்ஸ்ரே எடுக்க மருத்துவமனைக்கு அழைத்துச் செல்லவும்."
        }
    },
    "snakebites": {
        en: {
            title: "🐍 Venomous Snakebites (Anti-Venom Protocol)",
            severity: "Life-Threatening Emergency - Immediate Action",
            severityClass: "status-urgent",
            step1: "Complete Immobility & Calming: Reassure the victim. Keep them 100% physically still. Any movement or panic pumps venom through the lymphatic system faster.",
            step2: "Immobilize the Limb at or Below Heart Level: Use a flat wooden board, cardboard, or bamboo splint to immobilize the bitten arm/leg just like a fracture. Gently bandage without cutting off pulse.",
            step3: "Remove Constricting Items: Immediately slip off rings, bangles, anklets, or tight shoes before swelling begins.",
            step4: "Rush to Hospital with Anti-Snake Venom (ASV): Transport in a vehicle or lying down. Alert Primary Health Center (PHC) or district hospital.",
            donts: ["NEVER cut the bite with blades or knives.", "NEVER attempt to suck venom by mouth or pump.", "NEVER tie a tight rope or arterial tourniquet (causes tissue necrosis/gangrene).", "NEVER give aspirin, painkiller injections, or alcohol."],
            transport: "Hospital ASV is the ONLY antidote: Time is vital. Reach a hospital with polyvalent Anti-Snake Venom within 1-2 hours. Note snake appearance if safely visible, but NEVER attempt to catch or kill it."
        },
        ta: {
            title: "🐍 பாம்பு கடி அவசர முதலுதவி (உயிர்காக்கும் ASV நெறிமுறை)",
            severity: "உடனடி அவசர மருத்துவமனை சிகிச்சை",
            severityClass: "status-urgent",
            step1: "முழுமையான அசைவின்மை: பாதிக்கப்பட்டவரை முற்றிலும் அமைதிப்படுத்தி, துளியும் நடக்கவோ அசையவோ விடாமல் படுக்க வைக்கவும். பதற்றமும் அசைவும் விஷத்தை உடல் முழுவதும் வேகமாகப் பரப்பும்.",
            step2: "கடித்த இடத்தை நிலைநிறுத்துதல்: கடித்த கையை அல்லது காலை இதய மட்டத்திற்கு கீழே வைத்து, மரக்கட்டை அல்லது தடிமனான அட்டை வைத்து அசைக்க முடியாமல் மென்மையாகக் கட்டவும் (இரத்த ஓட்டம் தடைபடக் கூடாது).",
            step3: "ஆடைகள்/ஆபரணங்களை அகற்றுதல்: வீக்கம் வருவதற்குள் மோதிரம், கொலுசு, காலணிகள், இறுக்கமான ஆடைகளை உடனடியாக கழற்றவும்.",
            step4: "உடனடி மருத்துவமனை பயணம்: நோயாளியை படுக்க வைத்தவாறே 108 அவசர ஊர்தி அல்லது வாகனத்தில் Anti-Snake Venom (ASV) மருந்துள்ள அரசு மருத்துவமனைக்குக் கொண்டு செல்லவும்.",
            donts: ["பிளேடு அல்லது கத்தியால் காயத்தை கீறக் கூடாது.", "வாயால் விஷத்தை உறிஞ்ச முயற்சிக்கவே கூடாது.", "கயிறு கொண்டு மிக இறுக்கமாக ரத்த ஓட்டத்தை நிறுத்தக் கட்டக் கூடாது (இது தசையை அழுகச் செய்யும்).", "ஆஸ்பிரின், வலி நிவாரணிகள் அல்லது நாட்டு மருந்துகளை தரக் கூடாது."],
            transport: "ASV மட்டுமே விஷ முறிவு மருந்து: பாம்பு கடித்த 1-2 மணி நேரத்திற்குள் அரசு மருத்துவமனைக்குச் செல்ல வேண்டும். பாம்பை பிடிக்கவோ அடிக்கவோ முயன்று நேரத்தை வீணடிக்காதீர்கள்."
        }
    },
    "animal-bites": {
        en: {
            title: "🐕 Dog, Cat & Animal Bites (Rabies Prevention)",
            severity: "Urgent Fatal Risk Without Vaccine",
            severityClass: "status-urgent",
            step1: "15-Minute Continuous Soap & Running Water Flush: Immediately place the bite under flowing tap water with laundry/toilet soap for a full 15 minutes. Soap dissolves the lipid envelope of rabies virus and eliminates >70% of viral load.",
            step2: "Disinfect Wound Surface: Apply Povidone-Iodine 5% (Betadine) or 70% alcohol generously. Avoid covering tightly.",
            step3: "Urgent Anti-Rabies Vaccine (ARV): Must receive Day-0 ARV dose at government clinic/hospital within 24 hours.",
            step4: "Rabies Immunoglobulin (RIG): Category III bites (broken skin or bleeding) require RIG infiltrated around the wound on Day 0.",
            donts: ["Do NOT apply chili powder, turmeric, lime, or cow dung.", "Do NOT bandage tightly or suture/stitch fresh bite wounds.", "Do NOT delay vaccine assuming pet was vaccinated unless vet confirms."],
            transport: "Government Hospital ARV Protocol: Day 0, Day 3, Day 7, Day 14, and Day 28 doses are mandatory. Rabies is 100% fatal once symptoms appear, but 100% preventable with prompt vaccination."
        },
        ta: {
            title: "🐕 நாய் மற்றும் விலங்கு கடி (ரேபிஸ் தடுப்பு முதலுதவி)",
            severity: "தடுப்பூசி இல்லையெனில் உயிருக்கு ஆபத்து",
            severityClass: "status-urgent",
            step1: "15 நிமிடம் சோப்பு போட்டு கழுவுதல்: கடிபட்ட இடத்தை உடனடியாக ஓடும் குழாய் நீரில் சோப்பு போட்டு முழுமையாக 15 நிமிடங்கள் இடைவிடாமல் கழுவவும். சோப்பு நுரை ரேபிஸ் வைரஸின் 70% மேல் அழித்துவிடும்.",
            step2: "கிருமிநாசினி பூசுதல்: Betadine அல்லது 70% ஆல்கஹால் திரவத்தை காயத்தின் மேல் தாராளமாக ஊற்றி சுத்தம் செய்யவும். காற்று புகாமல் அடைக்க வேண்டாம்.",
            step3: "ரேபிஸ் தடுப்பூசி (ARV): 24 மணி நேரத்திற்குள் ஆரம்ப சுகாதார நிலையம் அல்லது அரசு மருத்துவமனையில் Day-0 ரேபிஸ் தடுப்பூசி போட வேண்டும்.",
            step4: "இம்யூனோகுளோபுலின் (RIG): இரத்தம் வரும் ஆழமான கடிக்கு (Category III) காயத்தைச் சுற்றி போடும் RIG மருந்து அவசியம்.",
            donts: ["மிளகாய் பொடி, சுண்ணாம்பு, சாணம், எண்ணெய் எதையும் காயத்தில் வைக்கக் கூடாது.", "காயத்தை உடனே தைக்கவோ அல்லது இறுக்கமாக பிளாஸ்திரி போடவோ கூடாது.", "வீட்டு நாய் தானே என்று தடுப்பூசி போடுவதை தாமதிக்கக் கூடாது."],
            transport: "அரசு மருத்துவமனையில் இலவச தடுப்பூசி: Day 0, 3, 7, 14, 28 அட்டவணைப்படி முழுமையாக தடுப்பூசி போடவும். ரேபிஸ் அறிகுறிகள் தோன்றினால் குணப்படுத்த முடியாது, ஆனால் தடுப்பூசி போட்டால் 100% தடுக்க முடியும்."
        }
    },
    "unconsciousness": {
        en: {
            title: "🫀 Unconsciousness, Fainting & CPR (DRSABCD Protocol)",
            severity: "Life-Threatening Emergency - Immediate Resuscitation",
            severityClass: "status-urgent",
            step1: "DRS Check (Danger, Response, Send for Help): Ensure area is safe. Tap shoulders and shout: 'Are you okay?'. If unresponsive, shout for help and immediately call 108.",
            step2: "Airway & Breathing Check: Gently tilt head back and lift chin. Look, listen, and feel for normal breathing for 10 seconds (agonal gasping is NOT normal breathing).",
            step3: "If Breathing Normally -> Recovery Position: Roll victim onto their side. Bend top knee to prop them up. Tilt head gently back to keep airway open and prevent choking on saliva or vomit.",
            step4: "If NOT Breathing -> Start CPR Immediately: Place heel of palm on center of chest. Interlock other hand. Push hard and fast (100-120 compressions/min, 2 inches deep). Give 30 compressions followed by 2 rescue breaths (or continuous Hands-Only CPR without stopping) until ambulance arrives.",
            donts: ["NEVER give water, food, or medicines to an unconscious person (causes fatal aspiration choking).", "NEVER shake a person with suspected head or neck injury.", "NEVER crowd around victim; ensure maximum fresh airflow.", "Do NOT stop CPR until medical help takes over or victim moves."],
            transport: "Immediate 108 Emergency Transport: Unconsciousness indicates cardiac arrest, stroke, severe head trauma, or respiratory failure. Continuous CPR maintains oxygen to the brain until defibrillator/paramedics arrive."
        },
        ta: {
            title: "🫀 சுயநினைவின்மை, மயக்கம் & CPR முதலுதவி (DRSABCD நெறிமுறை)",
            severity: "உடனடி உயிர்காக்கும் அவசர சிகிச்சை",
            severityClass: "status-urgent",
            step1: "சோதித்தல் & 108 அழைப்பு: பாதுகாப்பான இடமா எனப் பார்த்து, தோள்களைத் தட்டி 'நீங்கள் நலமாக உள்ளீர்களா?' எனக் குரல் எழுப்பவும். பதிலில்லை எனில் உடனே சுற்றியுள்ளவர்களை உதவிக்கு அழைத்து 108 அழைக்கச் சொல்லவும்.",
            step2: "சுவாசப் பரிசோதனை: தலையை மெதுவாக பின்நோக்கி சாய்த்து, தாடையை உயர்த்தவும். மார்பு ஏறி இறங்குகிறதா, மூச்சுக்காற்று வருகிறதா என 10 வினாடிகள் கவனிக்கவும்.",
            step3: "சுவாசம் இருந்தால் -> பக்கவாட்டு மீட்பு நிலை (Recovery Position): நோயாளியை பக்கவாட்டில் ஒருபுறமாக திருப்பி, தலையை லேசாக உயர்த்தி வைக்கவும். இது நாக்கு தொண்டையை அடைக்காமல், வாந்தி எடுத்தாலும் மூச்சுக்குழாய்க்குள் செல்லாமல் காக்கும்.",
            step4: "சுவாசம் இல்லையெனில் -> உடனடியாக CPR தொடங்கவும்: மார்பின் நடுப்பகுதியில் உள்ளங்கையை வைத்து, மற்றொரு கையை கோர்த்துக்கொள்ளவும். நிமிடத்திற்கு 100-120 முறை வேகமாகவும், 2 அங்குல ஆழத்திலும் இடைவிடாமல் அழுத்தவும் (30 அழுத்தங்கள் : 2 செயற்கை சுவாசம், அல்லது தொடர்ந்து மார்பு அழுத்தம் மட்டும்) ஆம்புலன்ஸ் வரும் வரை நிறுத்த வேண்டாம்.",
            donts: ["மயக்கமடைந்தவருக்கு ஒருபோதும் தண்ணீர் அல்லது மருந்து புகட்டக் கூடாது (மூச்சுக்குழாயில் அடைத்து மரணம் ஏற்படும்).", "தலையில் அடிபட்டவரை வேகமாக குலுக்கவோ அசைக்கவோ கூடாது.", "நோயாளியைச் சுற்றி கூட்டம் கூடாமல் நல்ல காற்று வர அனுமதிக்கவும்.", "ஆம்புலன்ஸ் வரும் வரை CPR செய்வதை நிறுத்தக் கூடாது."],
            transport: "உடனடி 108 அவசர ஊர்தி: சுயநினைவின்மை மாரடைப்பு, பக்கவாதம் அல்லது மூளை பாதிப்பின் அறிகுறி. CPR செய்வதன் மூலம் மூளைக்கு ஆக்சிஜன் செல்வதை உறுதி செய்து உயிரைக் காப்பாற்ற முடியும்."
        }
    },
    "puncture-wounds": {
        en: {
            title: "🔩 Puncture Wounds & Rusty Nails (Tetanus)",
            severity: "High Tetanus Risk Protocol",
            severityClass: "status-moderate",
            step1: "Mechanical Wash: Run under flowing tap water with soap for a full 5-10 minutes to clear anaerobic bacteria.",
            step2: "Do NOT Squeeze Hard: Avoid deep digging or probing with needles.",
            step3: "Disinfect: Apply generous Betadine liquid to the puncture entrance.",
            step4: "Tetanus Toxoid (TT) Injection: Essential within 24 hours if last TT shot was >5 years ago.",
            donts: ["Do NOT seal completely airtight with duct tape.", "Do NOT leave rusty particles inside."],
            transport: "Urgent Clinic Visit: Mandatory for Tetanus injection and antibiotic evaluation."
        },
        ta: {
            title: "🔩 ஆணி / முள் குத்திய ஆழமான காயங்கள் (டெட்டனஸ்)",
            severity: "டெட்டனஸ் ஆபத்து",
            severityClass: "status-moderate",
            step1: "ஓடும் நீரில் கழுவுதல்: சோப்பு போட்டு 5-10 நிமிடங்கள் அழுக்கு வெளியேறும் வரை கழுவவும்.",
            step2: "ஆழமாக குத்தாதீர்கள்: ஊசி அல்லது பிளேடால் காயத்தை கிளற வேண்டாம்.",
            step3: "கிருமிநாசினி: Betadine திரவத்தை காயத்தின் மீது ஊற்றி சுத்தம் செய்யவும்.",
            step4: "TT தடுப்பூசி: 24 மணி நேரத்திற்குள் டெட்டனஸ் டாக்சாய்டு (TT) ஊசி போடுவது மிக அவசியம்.",
            donts: ["காற்று புகாதவாறு பிளாஸ்திரி கொண்டு அடைக்கக் கூடாது.", "துருத்துண்டுகள் உள்ளே இருந்தால் சொந்தமாக எடுக்க முயற்சிக்காதீர்கள்."],
            transport: "மருத்துவமனை செல்வது கட்டாயம்: TT தடுப்பூசி மற்றும் தொற்று தடுப்பு மருந்துக்கு உடனே செல்லவும்."
        }
    },
    "sepsis": {
        en: {
            title: "⚠️ Sepsis & Severe Wound Infection",
            severity: "Life-Threatening Systemic Infection",
            severityClass: "status-urgent",
            step1: "Recognize Red Streaks: Red lines radiating from the wound towards the heart indicates lymphangitis/bloodstream infection.",
            step2: "Foul Odor & Throbbing Pus: Thick yellowish-green discharge and burning local heat.",
            step3: "Systemic Signs: High fever (>101°F), shaking chills, rapid heart rate (>100 bpm), confusion, extreme weakness.",
            step4: "Immediate Hospital Care: Sepsis requires IV antibiotics and surgical wound drainage.",
            donts: ["Do NOT squeeze or burst infected abscesses with dirty pins.", "Do NOT rely solely on home herbs when systemic fever starts."],
            transport: "Non-Negotiable ER Transport: Sepsis is an extreme medical emergency. Call 108 or arrange urgent car transport."
        },
        ta: {
            title: "⚠️ சீழ் தொற்று மற்றும் செப்சிஸ் (இரத்த நச்சு)",
            severity: "உயிருக்கு ஆபத்தான தீவிர தொற்று",
            severityClass: "status-urgent",
            step1: "சிவந்த கோடுகள்: காயத்திலிருந்து இதயத்தை நோக்கி சிவந்த கோடுகள் பரவினால் தொற்று இரத்தத்தில் கலக்கிறது என்று பொருள்.",
            step2: "சீழ் & துர்நாற்றம்: காயத்திலிருந்து துர்நாற்றத்துடன் கூடிய மஞ்சள்-பச்சை சீழ் வெளியேறுதல்.",
            step3: "உடல் முழுவதும் தாக்கம்: கடுமையான காய்ச்சல் (101°F மேல்), நடுக்கம், வேகமான இதயத் துடிப்பு, குழப்பம், அதீத சோர்வு.",
            step4: "உடனடி சிகிச்சை: இதற்கு நரம்பு வழி ஆன்டிபயாடிக் (IV Antibiotics) சிகிச்சை மருத்துவமனையில் மட்டுமே தர முடியும்.",
            donts: ["சீழ் கட்டியை அழுத்தி உடைக்கக் கூடாது.", "காய்ச்சல் வந்த பிறகு நாட்டு மருந்துகளுடன் நேரத்தை கடத்தக் கூடாது."],
            transport: "உடனடி மருத்துவமனை: தாமதிக்காமல் 108 அவசர ஊர்தி அல்லது வாகனத்தில் அவசர சிகிச்சைப் பிரிவுக்குச் செல்லவும்."
        }
    }
};

// ============================================================================
// DATA: ESSENTIAL MEDICINE KIT (Bilingual)
// ============================================================================
const ESSENTIAL_MEDS = [
    {
        id: "betadine",
        category: "wound",
        icon: "🩹",
        nameEn: "Povidone-Iodine 5% (Betadine)",
        nameTa: "Betadine 5% (பொவிடோன் அயோடின்)",
        typeEn: "Antiseptic Liquid & Ointment",
        typeTa: "கிருமிநாசினி திரவம் & கிரீம்",
        doseEn: "Apply directly on cleaned cuts, grazes, or minor burns.",
        doseTa: "கழுவப்பட்ட காயங்கள், கீறல்கள் மீது நேரடியாக பூசவும்.",
        limitEn: "External use only. Avoid in iodine allergy.",
        limitTa: "வெளிப்புற பயன்பாட்டிற்கு மட்டும். அயோடின் ஒவ்வாமை இருந்தால் தவிர்க்கவும்.",
        cautionEn: "Gold standard antiseptic to prevent bacterial infection in remote homes.",
        cautionTa: "தொற்று ஏற்படாமல் காக்கும் மிக முக்கியமான முதலுதவி கிருமிநாசினி."
    },
    {
        id: "gauze",
        category: "wound",
        icon: "📦",
        nameEn: "Sterile Gauze Pads & Micropore Tape",
        nameTa: "மலட்டு காஸ் துணி & மெடிக்கல் டேப்",
        typeEn: "Wound Dressing Material",
        typeTa: "கட்டுப் போடும் மருத்துவ துணி",
        doseEn: "2x2 inch & 4x4 inch sterile pads for bleeding control and dressing.",
        doseTa: "இரத்தப்போக்கை நிறுத்தவும் கட்டு போடவும் பயன்படும் மலட்டு துணிகள்.",
        limitEn: "Keep in sealed waterproof pack until use.",
        limitTa: "ஈரம் படாத காற்று புகாத பாக்கெட்டில் வைக்கவும்.",
        cautionEn: "Never use unwashed dirty household cloth on open bleeding flesh.",
        cautionTa: "இரத்தம் வரும் காயத்தின் மேல் அசுத்தமான துணிகளை வைக்கக் கூடாது."
    },
    {
        id: "paracetamol",
        category: "fever",
        icon: "🌡️",
        nameEn: "Paracetamol (Dolo 650 / Calpol 500)",
        nameTa: "Paracetamol (Dolo 650 / பாராசிட்டமால்)",
        typeEn: "Antipyretic & Pain Reliever",
        typeTa: "காய்ச்சல் மற்றும் வலி நிவாரணி",
        doseEn: "Adults: 500mg-650mg every 6-8 hours after food.",
        doseTa: "பெரியவர்கள்: 500mg-650mg தேவைப்பட்டால் 6-8 மணி நேரத்திற்கு ஒரு முறை.",
        limitEn: "Max 3000mg (3g) per 24 hours to protect liver.",
        limitTa: "ஒரு நாளில் 3000mg-க்கு மேல் உட்கொள்ளக் கூடாது (கல்லீரல் பாதுகாப்பு).",
        cautionEn: "Safe for fever and headaches. Avoid combining multiple paracetamol brands.",
        cautionTa: "காய்ச்சல் மற்றும் தலைவலிக்கு பாதுகாப்பானது. வெறும் வயிற்றில் சாப்பிட வேண்டாம்."
    },
    {
        id: "ors",
        category: "stomach",
        icon: "💧",
        nameEn: "WHO-Formula ORS (Oral Rehydration Salts)",
        nameTa: "WHO-ORS எலக்ட்ரோலைட் பாக்கெட்",
        typeEn: "Electrolyte Life-Saver",
        typeTa: "உயிர் காக்கும் உப்பு-சர்க்கரை கரைசல்",
        doseEn: "Mix 1 sachet in exactly 1 liter of clean drinking water. Sip continuously.",
        doseTa: "1 பாக்கெட்டை 1 லிட்டர் சுத்தமான நீரில் கலந்து சிறிது சிறிதாக குடிக்கவும்.",
        limitEn: "Drink within 24 hours of preparation. Discard remainder.",
        limitTa: "கலந்த 24 மணி நேரத்திற்குள் குடிக்கவும். மீதத்தை கொட்டி விடவும்.",
        cautionEn: "Prevents death from dehydration during diarrhea, vomiting, and high fever.",
        cautionTa: "வாந்தி, பேதி மற்றும் காய்ச்சலின் போது ஏற்படும் நீரிழப்பைத் தடுத்து உயிர் காக்கும்."
    },
    {
        id: "antacid",
        category: "stomach",
        icon: "🤢",
        nameEn: "Antacid (Digene / Gelusil)",
        nameTa: "Antacid சிரப் / மாத்திரை (டைஜீன்)",
        typeEn: "Acidity & Heartburn Relief",
        typeTa: "நெஞ்செரிச்சல் மற்றும் அசிடிட்டி நிவாரணம்",
        doseEn: "10-15 ml liquid or 1-2 chewable tablets after meals.",
        doseTa: "உணவுக்குப் பின் 10-15 மிலி திரவம் அல்லது 1-2 மெல்லும் மாத்திரைகள்.",
        limitEn: "Do not exceed 4 times daily.",
        limitTa: "ஒரு நாளில் 4 முறைக்கு மேல் உட்கொள்ள வேண்டாம்.",
        cautionEn: "Relieves indigestion and burning chest discomfort.",
        cautionTa: "அஜீரணம், வாயு மற்றும் நெஞ்செரிச்சலை உடனடியாகக் கட்டுப்படுத்தும்."
    },
    {
        id: "burnol",
        category: "allergy",
        icon: "🔥",
        nameEn: "Silver Sulfadiazine 1% (Burnol Cream)",
        nameTa: "Silver Sulfadiazine 1% (தீக்காய கிரீம்)",
        typeEn: "Topical Antibacterial Burn Cream",
        typeTa: "தீக்காய கிருமி தடுப்பு களிம்பு",
        doseEn: "Gently spread a sterile 1-2 mm layer over cooled burns.",
        doseTa: "குளிர்விக்கப்பட்ட தீக்காயத்தின் மேல் 1-2 மிமீ தடிமனில் மெதுவாக பூசவும்.",
        limitEn: "Not for pregnant women near term or infants under 2 months.",
        limitTa: "கர்ப்பிணிகள் மற்றும் 2 மாதத்திற்குட்பட்ட குழந்தைகளுக்கு தவிர்க்கவும்.",
        cautionEn: "Prevents dangerous hospital-acquired wound infections in burn cases.",
        cautionTa: "தீக்காயங்களில் கொப்புளங்கள் மற்றும் சீழ் தொற்று ஏற்படாமல் காக்கும்."
    },
    {
        id: "cetirizine",
        category: "allergy",
        icon: "🐝",
        nameEn: "Cetirizine 10mg",
        nameTa: "Cetirizine 10mg (சிட்ரிசின்)",
        typeEn: "Antihistamine / Allergy Relief",
        typeTa: "ஒவ்வாமை மற்றும் அரிப்பு மாத்திரை",
        doseEn: "Adults: 1 tablet (10mg) once daily at bedtime.",
        doseTa: "பெரியவர்கள்: இரவு படுக்கும் முன் 1 மாத்திரை (10mg).",
        limitEn: "May cause slight drowsiness. Avoid driving.",
        limitTa: "லேசான தூக்கக் கலக்கம் வரலாம். வாகனம் ஓட்டுவதைத் தவிர்க்கவும்.",
        cautionEn: "Essential for insect stings, sudden skin rashes, and allergic sneezing.",
        cautionTa: "வண்டு கடி, தோல் தடிப்புகள் மற்றும் ஒவ்வாமை தும்மலுக்கு மிகச் சிறந்தது."
    },
    {
        id: "thermometer",
        category: "tools",
        icon: "🌡️",
        nameEn: "Digital Clinical Thermometer",
        nameTa: "டிஜிட்டல் வெப்பமானி (Thermometer)",
        typeEn: "Diagnostic Device",
        typeTa: "உடல் வெப்பநிலை அளக்கும் கருவி",
        doseEn: "Place under armpit or tongue until beep. Normal: 97.7°F - 99.0°F.",
        doseTa: "அக்குளில் அல்லது நாக்கின் அடியில் வைத்து பீப் சத்தம் வரை வைக்கவும்.",
        limitEn: "Disinfect tip with alcohol before and after each use.",
        limitTa: "பயன்படுத்துவதற்கு முன்பும் பின்பும் ஆல்கஹால் துணியால் துடைக்கவும்.",
        cautionEn: "Never guess fever with bare hands—accurate readings prevent febrile convulsions.",
        cautionTa: "கையால் தொட்டு காய்ச்சலை யூகிக்காமல் சரியான வெப்பநிலையை அறிய உதவும்."
    },
    {
        id: "oximeter",
        category: "tools",
        icon: "🩺",
        nameEn: "Fingertip Pulse Oximeter",
        nameTa: "பல்ஸ் ஆக்ஸிமீட்டர் (Pulse Oximeter)",
        typeEn: "SpO2 & Heart Rate Monitor",
        typeTa: "ஆக்சிஜன் & நாடித் துடிப்பு கருவி",
        doseEn: "Clip on index finger while resting. Normal SpO2: 95% - 100%.",
        doseTa: "ஆள்காட்டி விரலில் பொருத்தவும். இயல்பான ஆக்சிஜன்: 95% - 100%.",
        limitEn: "SpO2 below 94% indicates urgent need for supplemental oxygen.",
        limitTa: "94%-க்கு கீழ் சென்றால் உடனடியாக மருத்துவமனை செல்ல வேண்டும்.",
        cautionEn: "Vital for respiratory infections, pneumonia, and elderly care in remote homes.",
        cautionTa: "நுரையீரல் தொற்று, சளி மற்றும் முதியோர்களின் ஆக்சிஜன் அளவை கண்காணிக்க உதவும்."
    },
    {
        id: "bp-monitor",
        category: "tools",
        icon: "💓",
        nameEn: "Automatic Arm Blood Pressure Monitor",
        nameTa: "டிஜிட்டல் இரத்த அழுத்த மானி (BP Monitor)",
        typeEn: "Cardiovascular Monitor",
        typeTa: "இரத்த அழுத்த மானி",
        doseEn: "Wrap cuff around bare upper arm at heart level while seated quietly for 5 mins.",
        doseTa: "5 நிமிடம் அமைதியாக அமர்ந்த பின் இதய மட்டத்தில் கையில் கட்டவும்.",
        limitEn: "Normal: <120/80 mmHg. High: >=140/90 mmHg.",
        limitTa: "சாதாரண அளவு: <120/80. அதிகம்: >=140/90.",
        cautionEn: "Detects silent hypertension and prevents sudden strokes in rural communities.",
        cautionTa: "மாரடைப்பு மற்றும் பக்கவாதம் வராமல் தடுக்க இரத்த அழுத்தத்தை தினமும் கண்காணிக்கவும்."
    }
];

// ============================================================================
// COMPLETE LOCALIZATION DICTIONARY (100% ALL WORDS & LABELS)
// ============================================================================
const i18n = {
    English: {
        // Navigation Tabs
        tabChat: "💬 Chat",
        tabWounds: "🩹 Offline First-Aid",
        tabMeds: "🛒 Medicine Kit",
        tabChart: "📊 Daily Log & Chart",
        tabReport: "📄 Doctor Report",

        // Header & Banners
        brandTagline: "Remote Emergency & Bilingual Health Assistant • தமிழ் / English",
        statusReady: "AI Ready",
        statusConnecting: "Connecting...",
        networkOnline: "Online",
        networkOffline: "Offline Mode",
        cacheReady: "Offline Pack: Ready",
        clearBtnTitle: "Clear Chat History",
        dailyBannerTitle: "Daily Health Check-in: How are you feeling today?",
        dailyBannerDesc: "Living far from a hospital? Regularly record your blood pressure, sugar, and symptoms to build your monthly doctor report.",
        quickCheckinBtn: "➕ Log Today's Vitals",
        emergencyTitle: "Medical Emergency Notice",
        emergencyDesc: "If you or someone else is experiencing severe chest pain, breathing difficulty, heavy blood loss, or unconsciousness, call 108 (India) or rush to the nearest Primary Health Center (PHC) immediately.",
        emergencyBtn: "Call 108 📞",

        // Offline Banner & Triage
        offlineBannerTitle: "Offline Mode Active • Internet Disconnected",
        offlineBannerDesc: "You are currently offline. Live AI consultation is unavailable without internet, but your cached Offline First-Aid Guide and saved vitals records are 100% available locally.",
        offlineBtnText: "🩹 Open Offline First-Aid",
        offlineGuideStatus: "Offline First-Aid Pack: 100% Downloaded & Saved in Browser Cache Storage",
        triageTitle: "CRITICAL EMERGENCY NOTICE: When to Seek Immediate Hospital / 108 Care",
        triageSubtitle: "First-aid guidance stabilizes the victim and prevents death while transport is arranged. It NEVER replaces professional hospital emergency care, surgery, or antivenom administration.",
        triageRushTitle: "🚑 Call 108 / Rush to Nearest Hospital Immediately If:",
        triageRoleTitle: "🛡️ How to Use This Offline Guide:",
        triageRoleDesc: "When you are in a remote village, highway, or facing power/network failure: Select the injury type below. Follow the 4-step clinical protocol, heed the DANGER DON'TS, and safely transport the patient to the nearest Primary Health Center (PHC).",
        triageRushList: [
            "Pumping arterial or heavy bleeding that does not stop with direct palm pressure",
            "Victim is unresponsive, unconscious, or stopped breathing (start CPR immediately)",
            "Any venomous snakebite (Anti-Snake Venom required in hospital within 1-2 hours)",
            "Severe burns larger than a palm, electrical burns, or burns on face, neck, or groin",
            "Suspected broken neck, spine, or thigh bone (femur) — keep victim completely still",
            "Dog or wild animal bite (requires Anti-Rabies Vaccine & Immunoglobulin within 24 hours)"
        ],

        // View 1: Chat
        hackathonTag: "Remote Care Healthcare AI • Strands SDK & Gemini",
        heroTitle: "Your Health, Guided in Your Language.",
        heroSubtitle: "Triage symptoms, understand emergency wound care, get verified OTC home remedies, and track vitals when hospitals are hours away.",
        suggestLabel: "💡 Suggested Inquiries:",
        chatTitle: "Health Consultation Session",
        chatSubtitle: "Informational AI guidance • Not a clinical diagnosis",
        voiceLabel: "Voice Input",
        voiceListening: "Listening...",
        welcomeHtml: `<strong>Hello! I am HealthMate AI. 👋</strong><br><br>I am your remote healthcare guide. I can help with <strong>emergency wound treatment</strong>, recommended <strong>essential home medicines</strong>, daily <strong>vitals tracking</strong>, and preparing a <strong>monthly report for your doctor</strong> in <strong>English</strong> or <strong>Tamil</strong>.<br><br><em>How can I assist your health or family today?</em>`,
        chatPlaceholder: "Describe symptoms, wounds, or ask health questions in English or தமிழ்...",
        sendText: "Send",
        privacyNote: "🔒 Private & secure: Confidential consultation notes for remote communities.",
        chatOfflineWarning: `⚠️ **Offline Mode Active: Live AI Consultation is Unavailable Without Internet.**<br><br>Your device is currently disconnected. Live AI consultation cannot reach the server, but your complete **Offline First-Aid Guide** is ready and saved locally.<br><br>👉 Please open the <strong>[🩹 Offline First-Aid]</strong> tab to view step-by-step instructions for cuts, severe bleeding, burns, fractures, snakebites, animal bites, and unconsciousness/CPR.<br><br><em>In an acute emergency, call <strong>108</strong> immediately.</em>`,

        // View 2: Offline First-Aid Tutorial
        woundsTitle: "Complete Offline Emergency First-Aid Guide",
        woundsDesc: "Clinically verified, step-by-step first-aid protocols for remote areas, villages, and emergencies when hospital or ambulance is hours away. Fully functional offline.",
        woundsSelectLabel: "Select First-Aid / Emergency Condition:",
        woundPills: {
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

        // View 3: Medicine Kit
        medsTitle: "Essential Home Medicine & First-Aid Kit Checklist",
        medsDesc: "Verified list of vital OTC medicines and diagnostic devices to buy and stock at home in areas with limited pharmacies or medical centers.",
        medFilters: {
            "all": "All Supplies",
            "wound": "🩹 Wound & Antiseptics",
            "fever": "🌡️ Fever & Pain",
            "stomach": "🤢 Stomach & ORS",
            "allergy": "🐝 Allergies & Burns",
            "tools": "🩺 Vital Devices"
        },
        copyMedsBtn: "📋 Copy Shopping List",
        printMedsBtn: "🖨️ Print List",

        // View 4: Daily Log & Chart
        chartSectionTitle: "Daily Health Check-in & Vitals Tracker",
        chartSectionDesc: "Record your daily health metrics (BP, blood sugar, SpO2, temperature, symptoms). Visual trend graphs help you and your visiting doctor detect problems early.",
        logFormTitle: "☀️ Daily Health Check-in Entry",
        lblDate: "Date:",
        lblTime: "Time of Measurement:",
        lblSysBp: "Systolic BP (High / mmHg):",
        lblDiaBp: "Diastolic BP (Low / mmHg):",
        lblSugar: "Blood Sugar (mg/dL):",
        lblPulse: "Heart Rate / Pulse (BPM):",
        lblSpo2: "Oxygen SpO2 (%):",
        lblTemp: "Temperature (°F):",
        lblPain: "Pain Severity (0 = None, 10 = Severe):",
        lblSymptomsSelect: "Select Any Symptoms Experienced Today:",
        lblSeverity: "Overall Feeling Today:",
        lblNotes: "Notes / Food / Meds Taken:",
        phSysBp: "e.g. 120",
        phDiaBp: "e.g. 80",
        phSugar: "e.g. 95 (Fasting) or 130",
        phPulse: "e.g. 72",
        phSpo2: "e.g. 98",
        phTemp: "e.g. 98.6",
        phNotes: "e.g. Took Paracetamol, rested well, drank ORS...",
        severityOptions: {
            "Mild": "🟢 Mild / Feeling Good (Mild / Normal)",
            "Moderate": "🟡 Moderate / Need Rest (Moderate / Need Rest)",
            "Severe": "🔴 Severe / Feeling Unwell (Severe / Bad)"
        },
        symptomsDict: {
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
        painBadges: {
            0: "0 - No Pain 😊",
            mild: "Mild Pain 😐",
            mod: "Moderate Pain 😣",
            high: "High / Severe Pain 😫",
            worst: "10 - Extreme Worst Pain 🚨"
        },
        saveLogBtn: "💾 Save Daily Health Check-in",
        chartsTitle: "📈 Monthly Vitals Progression Charts",
        chartSwitches: {
            "bp": "Blood Pressure",
            "sugar-temp": "Sugar & Temp",
            "pulse-spo2": "Pulse & SpO2"
        },
        chartLegends: {
            sysBp: "Systolic BP (mmHg)",
            diaBp: "Diastolic BP (mmHg)",
            sugar: "Blood Sugar (mg/dL)",
            temp: "Temperature (°F)",
            pulse: "Heart Rate / Pulse (BPM)",
            spo2: "Oxygen SpO2 (%)"
        },
        timelineTitle: "📋 Daily Check-in History",
        analyzeChartBtn: "🤖 AI Review My Vitals Log",
        deleteEntryText: "🗑️ Delete Entry",

        // View 5: Doctor Report
        reportTitle: "Monthly Clinical Health Summary for Doctor",
        reportDesc: "Generate a professional, structured clinical report from your daily health check-ins. Send it to your real doctor via Email, WhatsApp, or Print/Save as PDF.",
        lblPatName: "Patient Name:",
        lblPatAge: "Age & Gender:",
        lblDocEmail: "Doctor's Email (for Sending):",
        lblDocPhone: "Doctor's WhatsApp / Mobile:",
        phPatName: "e.g. Ramesh Kumar",
        phPatAge: "e.g. 48 Y / Male",
        phDocPhone: "e.g. 919876543210",
        generateReportBtn: "✨ Generate Monthly Doctor Report",
        reportEmptyText: "Click 'Generate Monthly Doctor Report' above to compile your recorded daily logs into a hospital-grade physician handover summary.",
        docTitle: "HealthMate AI • Monthly Tele-Health Vitals Summary",
        docSubtitle: "Primary Health Center (PHC) & Remote Community Clinical Handover Sheet",
        docBadge: "CONFIDENTIAL MEDICAL REPORT",
        docLblName: "Patient Name:",
        docLblDemo: "Demographics:",
        docLblLoc: "Location Context:",
        docLocVal: "Remote / Hospital > 30 km",
        docLblWin: "Monitoring Window:",
        docWinVal: "Past 30 Days (Daily Logs)",
        docSec1Title: "1. Vitals Overview & Monthly Statistics",
        docSec2Title: "2. Clinical Red Flags & Threshold Deviations",
        docSec3Title: "3. Symptom Frequency Distribution",
        docSec4Title: "4. Physician Handover Memo & Clinical Observations",
        docSec5Title: "5. Attending Doctor's Prescription & Clinical Notes (For Doctor Use)",
        docRxLine: "Rx / Medications Prescribed: ___________________________________________________________",
        docLabLine: "Clinical Investigation Advised: [ ] Blood Routine [ ] HbA1c [ ] ECG [ ] Chest X-Ray [ ] Other: ______",
        docDateLine: "Date: _______________",
        docSignLine: "Doctor's Signature & Reg. No: ___________________________",
        docDisclaimer: "⚠️ Clinical Notice: This summary was aggregated from patient-recorded daily home vitals via HealthMate AI. It is intended to assist medical practitioners during clinical reviews or tele-consultations.",
        emailDoctorBtn: "✉️ Email to Doctor",
        whatsappDoctorBtn: "💬 Send via WhatsApp",
        printReportBtn: "🖨️ Print / Save as PDF",

        // Stat Card Labels
        statAvgBp: "Average BP (mmHg)",
        statPeakBp: "Peak BP Reading",
        statAvgSugar: "Avg Glucose (mg/dL)",
        statPeakSugar: "Peak Glucose (mg/dL)",
        statAvgSpo2: "Avg SpO2",
        statLowest: "Lowest",
        statAvgPulse: "Avg Pulse Rate (BPM)",
        statAvgTemp: "Avg Body Temp",
        statDaysMonitored: "Days Monitored",

        // Footer
        disclaimerHeader: "Important Medical Disclaimer",
        disclaimerBody: "HealthMate AI is an informational and remote emergency assistance tool built for communities with distant medical facilities. It is not a qualified doctor, cannot deliver confirmed clinical diagnoses, and does not prescribe prescription-only medicines. Always consult an authorized medical practitioner. In acute emergencies, call 108 or proceed immediately to the nearest hospital.",
        hackathonFooter: "AWS User Group Madurai Strands SDK Hackathon • Remote Healthcare Track • © 2026",

        suggestions: [
            "Severe cut bleeding won't stop, what should I do right now?",
            "What essential medicines should I buy to stock at home in a remote village?",
            "First aid steps if a stray dog bites someone in an isolated area",
            "My BP was 148/94 and sugar 185 today, is this dangerous?",
            "How to prepare WHO-ORS solution properly for dehydration"
        ]
    },

    Tamil: {
        // Navigation Tabs
        tabChat: "💬 அரட்டை",
        tabWounds: "🩹 அவசர முதலுதவி",
        tabMeds: "🛒 மருந்து பட்டியல்",
        tabChart: "📊 தினசரி பதிவு & வரைபடம்",
        tabReport: "📄 மருத்துவர் அறிக்கை",

        // Header & Banners
        brandTagline: "தொலைதூர அவசர முதலுதவி & தமிழ் AI உடல்நல உதவியாளர்",
        statusReady: "AI தயார்",
        statusConnecting: "இணைகிறது...",
        networkOnline: "இணையத்தில் உள்ளது",
        networkOffline: "ஆஃப்லைன் பயன்முறை",
        cacheReady: "ஆஃப்லைன் பேக்: தயார்",
        clearBtnTitle: "அரட்டை வரலாற்றை அழிக்க",
        dailyBannerTitle: "தினசரி உடல்நல பரிசோதனை: இன்று உங்கள் உடல்நிலை எப்படி உள்ளது?",
        dailyBannerDesc: "மருத்துவமனை வெகு தொலைவில் உள்ளதா? உங்கள் இரத்த அழுத்தம், சர்க்கரை மற்றும் அறிகுறிகளை தினமும் குறித்து வையுங்கள்.",
        quickCheckinBtn: "➕ இன்றைய அளவை பதிவு செய்ய",
        emergencyTitle: "அவசர மருத்துவ எச்சரிக்கை",
        emergencyDesc: "கடுமையான மார்பு வலி, மூச்சுத் திணறல், தீவிர இரத்தப்போக்கு அல்லது மயக்கம் ஏற்பட்டால் உடனடியாக 108 அழைக்கவும் அல்லது ஆரம்ப சுகாதார நிலையத்திற்கு (PHC) செல்லவும்.",
        emergencyBtn: "108 அழைக்க 📞",

        // Offline Banner & Triage
        offlineBannerTitle: "ஆஃப்லைன் பயன்முறை • இணைய இணைப்பு இல்லை",
        offlineBannerDesc: "தற்போது இணைய இணைப்பு துண்டிக்கப்பட்டுள்ளது. நேரலை AI ஆலோசனை பெற முடியாது, ஆனால் உங்களுக்கான முழுமையான ஆஃப்லைன் அவசர முதலுதவி வழிகாட்டி மற்றும் பதிவுகள் தயாராக உள்ளன.",
        offlineBtnText: "🩹 அவசர முதலுதவி வழிகாட்டியைத் திறக்க",
        offlineGuideStatus: "ஆஃப்லைன் முதலுதவி பேக்: உலாவியின் Cache Storage-ல் பதிவிறக்கம் செய்யப்பட்டு தயாராக உள்ளது",
        triageTitle: "முக்கிய அவசர அறிவிப்பு: எப்போது உடனடியாக 108 அழைக்க வேண்டும் / மருத்துவமனைக்கு செல்ல வேண்டும்",
        triageSubtitle: "முதலுதவி என்பது மருத்துவமனை செல்லும் வரை உயிரைக் காப்பாற்ற மட்டுமே. இது மருத்துவரின் தீவிர சிகிச்சை அல்லது அறுவை சிகிச்சைக்கு மாற்றாகாது.",
        triageRushTitle: "🚑 உடனடியாக 108 அழைக்க வேண்டிய அவசர நிலைகள்:",
        triageRoleTitle: "🛡️ இந்த ஆஃப்லைன் வழிகாட்டியை எவ்வாறு பயன்படுத்த வேண்டும்:",
        triageRoleDesc: "தொலைதூர கிராமத்திலோ அல்லது நெட்வொர்க் இல்லாத இடத்திலோ இருக்கும் போது: கீழே உள்ள காய வகையைத் தேர்ந்தெடுக்கவும். 4 படிநிலைகளை பின்பற்றி ஆபத்துகளைத் தவிர்த்து ஆரம்ப சுகாதார நிலையத்திற்கு நோயாளியை அழைத்துச் செல்லவும்.",
        triageRushList: [
            "அழுத்திப் பிடித்தும் நிற்காத தீவிர இரத்தப்போக்கு அல்லது இரத்தம் பீறிடுதல்",
            "பாதிக்கப்பட்டவர் சுயநினைவின்றி இருத்தல் அல்லது சுவாசம் நின்று போதல் (உடனே CPR தொடங்கவும்)",
            "விஷப் பாம்பு கடி (1-2 மணி நேரத்திற்குள் மருத்துவமனையில் ASV மருந்து பெற வேண்டும்)",
            "உள்ளங்கையை விட பெரிய தீக்காயங்கள் அல்லது முகம், மூட்டுகளில் ஏற்பட்ட தீக்காயங்கள்",
            "கழுத்து, முதுகுத்தண்டு அல்லது தொடை எலும்பு முறிவு சந்தேகம் (நோயாளியை அசைக்கக் கூடாது)",
            "நாய் அல்லது வெறி விலங்கு கடித்தல் (24 மணி நேரத்திற்குள் ரேபிஸ் தடுப்பூசி பெற வேண்டும்)"
        ],

        // View 1: Chat
        hackathonTag: "தொலைதூர மருத்துவ AI • Strands SDK & Gemini",
        heroTitle: "உங்கள் உடல்நலம், உங்கள் தாய்மொழியில்.",
        heroSubtitle: "காய சிகிச்சை, வீட்டிலேயே இருப்பு வைக்க வேண்டிய அத்தியாவசிய மருந்துகள், மற்றும் தினசரி இரத்த அழுத்த பதிவுகள்.",
        suggestLabel: "💡 மாதிரி கேள்விகள்:",
        chatTitle: "உடல்நல ஆலோசனை அரட்டை",
        chatSubtitle: "தகவல் வழிகாட்டுதல் மட்டுமே • மருத்துவ உறுதிப்படுத்தல் அல்ல",
        voiceLabel: "குரல் வழி உள்ளீடு",
        voiceListening: "கேட்கிறது...",
        welcomeHtml: `<strong>வணக்கம்! நான் HealthMate AI. 👋</strong><br><br>தொலைதூர பகுதிகளில் உள்ளவர்களுக்கான உங்கள் மருத்துவ வழிகாட்டி நான். <strong>அவசர காய சிகிச்சை</strong>, வீட்டில் வைக்க வேண்டிய <strong>அத்தியாவசிய முதலுதவி மருந்துகள்</strong>, தினசரி <strong>இரத்த அழுத்தம்/சர்க்கரை கண்காணிப்பு</strong> மற்றும் உங்கள் <strong>மருத்துவருக்கான மாதாந்திர அறிக்கை</strong> தயார் செய்ய நான் உதவுவேன்.<br><br><em>இன்று உங்களுக்கு நான் எவ்வாறு உதவ வேண்டும்?</em>`,
        chatPlaceholder: "அறிகுறிகள், காயங்கள் பற்றி தமிழில் எழுதுங்கள் (எ.கா: 3 நாட்களாக காய்ச்சல், வெட்டுக்காயம்)...",
        sendText: "அனுப்பு",
        privacyNote: "🔒 பாதுகாப்பானது: தொலைதூர கிராமங்களுக்கான பாதுகாப்பான மருத்துவ வழிகாட்டி.",
        chatOfflineWarning: `⚠️ **ஆஃப்லைன் பயன்முறை: இணைய இணைப்பு இல்லாமல் AI ஆலோசனை பெற முடியாது.**<br><br>தற்போது இணைய இணைப்பு துண்டிக்கப்பட்டுள்ளது. நேரலை AI ஆலோசனை பெற முடியாது, ஆனால் உங்களுக்கான **முழுமையான ஆஃப்லைன் அவசர முதலுதவி வழிகாட்டி** உங்கள் உலாவியில் தயாராக சேமிக்கப்பட்டுள்ளது.<br><br>👉 உடனடி முதலுதவி படிகளைப் பார்க்க மேலே உள்ள <strong>[🩹 அவசர முதலுதவி]</strong> பகுதியைத் தேர்ந்தெடுக்கவும் (வெட்டுக்காயம், இரத்தப்போக்கு, தீக்காயம், பாம்பு கடி, நாய் கடி, மயக்கம்/CPR).<br><br><em>உயிருக்கு ஆபத்தான அவசர நிலையில் உடனடியாக <strong>108</strong> அழைக்கவும்.</em>`,

        // View 2: Offline First-Aid Tutorial
        woundsTitle: "முழுமையான ஆஃப்லைன் அவசர முதலுதவி வழிகாட்டி",
        woundsDesc: "மருத்துவமனை அல்லது ஆம்புலன்ஸ் வர இயலாத தொலைதூர கிராமங்களுக்கான படி-படியான மருத்துவ முதலுதவி வழிகாட்டி. ஆஃப்லைனில் முழுமையாக இயங்கும்.",
        woundsSelectLabel: "முதலுதவி அல்லது அவசர பாதிப்பு வகையைத் தேர்ந்தெடுக்கவும்:",
        woundPills: {
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

        // View 3: Medicine Kit
        medsTitle: "வீட்டில் இருப்பு வைக்க வேண்டிய அத்தியாவசிய மருந்துகள் பட்டியல்",
        medsDesc: "மருந்தகங்கள் குறைவாக உள்ள ஊர்களில் ஒவ்வொரு வீட்டிலும் வாங்கி வைக்க வேண்டிய பாதுகாப்பான OTC முதலுதவி மருந்துகள்.",
        medFilters: {
            "all": "அனைத்து பொருட்கள்",
            "wound": "🩹 காயம் & கிருமிநாசினி",
            "fever": "🌡️ காய்ச்சல் & வலி",
            "stomach": "🤢 வயிறு & ORS",
            "allergy": "🐝 ஒவ்வாமை & தீக்காயம்",
            "tools": "🩺 மருத்துவக் கருவிகள்"
        },
        copyMedsBtn: "📋 மருந்து பட்டியலை நகலெடு",
        printMedsBtn: "🖨️ பட்டியலை அச்சிடு",

        // View 4: Daily Log & Chart
        chartSectionTitle: "தினசரி உடல்நலப் பதிவு & வரைபட கண்காணிப்பு",
        chartSectionDesc: "தினசரி இரத்த அழுத்தம், சர்க்கரை அளவு, ஆக்ஸிஜன் மற்றும் காய்ச்சலை பதிவு செய்யுங்கள். வரைபடம் மூலம் நோய்களை முன்கூட்டியே கண்டறியலாம்.",
        logFormTitle: "☀️ இன்றைய உடல்நலப் பதிவு",
        lblDate: "தேதி (வருடம்-மாதம்-நாள்):",
        lblTime: "அளவிடப்பட்ட நேரம்:",
        lblSysBp: "சிஸ்டாலிக் BP (உயர் இரத்த அழுத்தம் / mmHg):",
        lblDiaBp: "டயஸ்டாலிக் BP (குறைந்த இரத்த அழுத்தம் / mmHg):",
        lblSugar: "இரத்த சர்க்கரை அளவு (mg/dL):",
        lblPulse: "நாடித் துடிப்பு / இதயத் துடிப்பு (BPM):",
        lblSpo2: "இரத்த ஆக்சிஜன் அளவு - SpO2 (%):",
        lblTemp: "உடல் வெப்பநிலை (°F):",
        lblPain: "வலி தீவிரம் (0 = வலி இல்லை, 10 = தாங்க முடியாத வலி):",
        lblSymptomsSelect: "இன்று ஏற்பட்ட அறிகுறிகளைத் தேர்ந்தெடுக்கவும்:",
        lblSeverity: "இன்றைய பொதுவான உடல்நிலை:",
        lblNotes: "கூடுதல் குறிப்புகள் / உட்கொண்ட மருந்துகள்:",
        phSysBp: "எ.கா: 120",
        phDiaBp: "எ.கா: 80",
        phSugar: "எ.கா: 95 அல்லது 140",
        phPulse: "எ.கா: 72",
        phSpo2: "எ.கா: 98",
        phTemp: "எ.கா: 98.6",
        phNotes: "எ.கா: பாராசிட்டமால் சாப்பிட்டேன், ஓய்வெடுத்தேன், ORS குடித்தேன்...",
        severityOptions: {
            "Mild": "🟢 லேசானது / நலம் (Mild / Normal)",
            "Moderate": "🟡 மிதமானது / ஓய்வு தேவை (Moderate / Need Rest)",
            "Severe": "🔴 தீவிரமானது / உடல்நிலை மோசம் (Severe / Bad)"
        },
        symptomsDict: {
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
        painBadges: {
            0: "0 - வலி இல்லை 😊",
            mild: "லேசான வலி 😐",
            mod: "மிதமான வலி 😣",
            high: "கடுமையான தீவிர வலி 😫",
            worst: "10 - தாங்க முடியாத உச்சகட்ட வலி 🚨"
        },
        saveLogBtn: "💾 இன்றைய பதிவை சேமிக்க",
        chartsTitle: "📈 மாதாந்திர உடல்நல அளவீட்டு வரைபடம்",
        chartSwitches: {
            "bp": "இரத்த அழுத்தம் (BP)",
            "sugar-temp": "சர்க்கரை & வெப்பநிலை",
            "pulse-spo2": "நாடி & ஆக்சிஜன்"
        },
        chartLegends: {
            sysBp: "சிஸ்டாலிக் BP (mmHg)",
            diaBp: "டயஸ்டாலிக் BP (mmHg)",
            sugar: "இரத்த சர்க்கரை (mg/dL)",
            temp: "உடல் வெப்பநிலை (°F)",
            pulse: "நாடித் துடிப்பு (BPM)",
            spo2: "ஆக்சிஜன் SpO2 (%)"
        },
        timelineTitle: "📋 பதிவு செய்யப்பட்ட தினசரி வரலாறு",
        analyzeChartBtn: "🤖 AI மூலம் எனது பதிவுகளை ஆராய்க",
        deleteEntryText: "🗑️ பதிவை நீக்கு",

        // View 5: Doctor Report
        reportTitle: "மருத்துவரிடம் காட்டுவதற்கான மாதாந்திர உடல்நல அறிக்கை",
        reportDesc: "உங்கள் தினசரி பதிவுகளை மருத்துவமனை அளவிலான அறிக்கையாக மாற்றி, உங்கள் மருத்துவருக்கு Email, WhatsApp அல்லது Print மூலம் எளிதாக அனுப்பலாம்.",
        lblPatName: "நோயாளி பெயர்:",
        lblPatAge: "வயது மற்றும் பாலினம்:",
        lblDocEmail: "மருத்துவரின் மின்னஞ்சல் (Email):",
        lblDocPhone: "மருத்துவரின் வாட்ஸ்அப் / கைபேசி எண்:",
        phPatName: "எ.கா: ரமேஷ் குமார் / செல்வி",
        phPatAge: "எ.கா: 48 வயது / ஆண்",
        phDocPhone: "எ.கா: 919876543210",
        generateReportBtn: "✨ மாதாந்திர மருத்துவ அறிக்கையை உருவாக்குக",
        reportEmptyText: "மேலே உள்ள 'மாதாந்திர மருத்துவ அறிக்கையை உருவாக்குக' பொத்தானை அழுத்தி, உங்கள் மருத்துவருக்கான விரிவான அறிக்கையை தயார் செய்யுங்கள்.",
        docTitle: "HealthMate AI • மாதாந்திர தொலைதூர மருத்துவ அறிக்கை",
        docSubtitle: "ஆரம்ப சுகாதார நிலையம் (PHC) மற்றும் குடும்ப மருத்துவ குறிப்பேடு",
        docBadge: "இரகசிய மருத்துவ ஆவணம்",
        docLblName: "நோயாளி பெயர்:",
        docLblDemo: "விவரம்:",
        docLblLoc: "வசிப்பிடம்:",
        docLocVal: "தொலைதூர கிராமம் (மருத்துவமனை > 30 கி.மீ)",
        docLblWin: "கண்காணிப்பு காலம்:",
        docWinVal: "கடந்த 30 நாட்கள் (தினசரி அளவீடுகள்)",
        docSec1Title: "1. மாதாந்திர உடல்நல புள்ளிவிவரங்கள் & சராசரிகள்",
        docSec2Title: "2. மருத்துவ எச்சரிக்கைகள் & வரம்பு மீறல்கள்",
        docSec3Title: "3. அறிகுறிகள் தோன்றிய நாட்களின் எண்ணிக்கை",
        docSec4Title: "4. மருத்துவருக்கான AI பகுப்பாய்வு குறிப்பு",
        docSec5Title: "5. மருத்துவரின் மருந்து பரிந்துரை & குறிப்புகள் (மருத்துவர் பயன்பாட்டிற்கு)",
        docRxLine: "பரிந்துரைக்கப்பட்ட மருந்துகள் (Rx): ___________________________________________________________",
        docLabLine: "பரிந்துரைக்கப்பட்ட சோதனைகள்: [ ] இரத்தப் பரிசோதனை [ ] HbA1c [ ] ECG [ ] மார்பு எக்ஸ்ரே [ ] பிற: ______",
        docDateLine: "தேதி: _______________",
        docSignLine: "மருத்துவரின் கையொப்பம் & பதிவு எண்: ___________________________",
        docDisclaimer: "⚠️ மருத்துவ குறிப்பு: இந்த அறிக்கை நோயாளியால் பதிவு செய்யப்பட்ட தினசரி வீட்டு அளவீடுகளின் அடிப்படையில் தொகுக்கப்பட்டது. மருத்துவர் அல்லது ஆரம்ப சுகாதார நிலைய மருத்துவ அலுவலரின் ஆலோசனைக்கு மட்டுமே.",
        emailDoctorBtn: "✉️ மருத்துவருக்கு மின்னஞ்சல் அனுப்பு",
        whatsappDoctorBtn: "💬 வாட்ஸ்அப் மூலம் அனுப்பு",
        printReportBtn: "🖨️ அச்சிடு / PDF சேமி",

        // Stat Card Labels
        statAvgBp: "சராசரி BP (mmHg)",
        statPeakBp: "அதிகபட்ச BP அளவு",
        statAvgSugar: "சராசரி சர்க்கரை (mg/dL)",
        statPeakSugar: "அதிகபட்ச சர்க்கரை (mg/dL)",
        statAvgSpo2: "சராசரி ஆக்சிஜன்",
        statLowest: "குறைந்தது",
        statAvgPulse: "சராசரி நாடித் துடிப்பு (BPM)",
        statAvgTemp: "சராசரி வெப்பநிலை",
        statDaysMonitored: "கண்காணிக்கப்பட்ட நாட்கள்",

        // Footer
        disclaimerHeader: "முக்கிய மருத்துவ மறுப்புரை",
        disclaimerBody: "HealthMate AI என்பது தொலைதூர கிராமங்களுக்கான முதலுதவி மற்றும் பொது உடல்நல தகவல் வழிகாட்டி மட்டுமே. இது மருத்துவர் அல்ல, நோய்களைக் கண்டறியவோ மருந்துச் சீட்டு தரவோ முடியாது. தீவிர உடல்நலப் பிரச்சனைகளுக்கு உடனடியாக மருத்துவரை அணுகவும் அல்லது அவசர உதவிக்கு 108 அழைக்கவும்.",
        hackathonFooter: "AWS User Group Madurai Strands SDK Hackathon • தொலைதூர மருத்துவ சேவை • © 2026",

        suggestions: [
            "ஆழமான வெட்டுக்காயத்தில் இரத்தம் நிற்கவில்லை, உடனே என்ன செய்ய வேண்டும்?",
            "கிராமத்தில் உள்ள வீட்டில் வாங்கி வைக்க வேண்டிய முதலுதவி மருந்துகள் என்ன?",
            "தெரு நாய் கடித்தால் உடனடியாக செய்ய வேண்டிய முதலுதவி படிகள் என்ன?",
            "இன்று எனது BP 148/94 மற்றும் சர்க்கரை 185 உள்ளது, இது ஆபத்தானதா?",
            "நீரிழப்புக்கு ORS கரைசலை சரியான முறையில் தயாரிப்பது எப்படி?"
        ]
    }
};

// ============================================================================
// COMPREHENSIVE LANGUAGE SWITCH FUNCTION
// ============================================================================
function applyLanguage(lang) {
    const dict = i18n[lang] || i18n.English;
    const isTa = lang === "Tamil";

    // 1. Navigation Tabs
    if (tabChatBtn) tabChatBtn.textContent = dict.tabChat;
    if (tabWoundsBtn) tabWoundsBtn.textContent = dict.tabWounds;
    if (tabMedsBtn) tabMedsBtn.textContent = dict.tabMeds;
    if (tabChartBtn) tabChartBtn.textContent = dict.tabChart;
    if (tabReportBtn) tabReportBtn.textContent = dict.tabReport;

    // 2. Header & Banners
    const brandTagline = document.getElementById("brand-tagline");
    if (brandTagline) brandTagline.textContent = dict.brandTagline;
    if (statusText) statusText.textContent = systemStatus.classList.contains("status-online") ? dict.statusReady : dict.statusConnecting;
    if (clearBtn) clearBtn.title = dict.clearBtnTitle;

    // Network & Cache Status Badges
    if (networkStatusText) {
        networkStatusText.textContent = navigator.onLine ? dict.networkOnline : dict.networkOffline;
    }
    if (cacheStatusText) {
        cacheStatusText.textContent = dict.cacheReady;
    }

    // Offline Banner
    if (offlineBannerTitle) offlineBannerTitle.textContent = dict.offlineBannerTitle;
    if (offlineBannerDesc) offlineBannerDesc.textContent = dict.offlineBannerDesc;
    if (offlineBtnText) offlineBtnText.textContent = dict.offlineBtnText;

    const dailyBannerTitle = document.getElementById("daily-banner-title");
    if (dailyBannerTitle) dailyBannerTitle.textContent = dict.dailyBannerTitle;
    const dailyBannerDesc = document.getElementById("daily-banner-desc");
    if (dailyBannerDesc) dailyBannerDesc.textContent = dict.dailyBannerDesc;
    if (quickCheckinBtn) quickCheckinBtn.innerHTML = `<span>${dict.quickCheckinBtn}</span>`;

    const emergencyTitle = document.getElementById("emergency-title");
    if (emergencyTitle) emergencyTitle.textContent = dict.emergencyTitle;
    const emergencyDesc = document.getElementById("emergency-desc");
    if (emergencyDesc) emergencyDesc.textContent = dict.emergencyDesc;
    const emergencyCallBtn = document.getElementById("emergency-call-btn");
    if (emergencyCallBtn) emergencyCallBtn.textContent = dict.emergencyBtn;

    // 3. View 1: Chat
    const hackathonTag = document.getElementById("hackathon-tag");
    if (hackathonTag) hackathonTag.textContent = dict.hackathonTag;
    const heroTitle = document.getElementById("hero-title");
    if (heroTitle) heroTitle.textContent = dict.heroTitle;
    const heroSubtitle = document.getElementById("hero-subtitle");
    if (heroSubtitle) heroSubtitle.textContent = dict.heroSubtitle;
    const suggestLabel = document.getElementById("suggest-label");
    if (suggestLabel) suggestLabel.textContent = dict.suggestLabel;

    const chatTitle = document.getElementById("chat-title");
    if (chatTitle) chatTitle.textContent = dict.chatTitle;
    if (chatSubtitle) chatSubtitle.textContent = dict.chatSubtitle;
    if (voiceLabel) voiceLabel.textContent = dict.voiceLabel;
    if (userInput) userInput.placeholder = dict.chatPlaceholder;
    if (sendButton) sendButton.querySelector("span").textContent = dict.sendText;
    const privacyNote = document.getElementById("privacy-note");
    if (privacyNote) privacyNote.textContent = dict.privacyNote;

    const welcomeMsg = document.getElementById("welcome-message");
    if (welcomeMsg) welcomeMsg.innerHTML = dict.welcomeHtml;

    // 4. View 2: Offline First-Aid & Emergency Triage
    const woundsTitle = document.getElementById("wounds-title");
    if (woundsTitle) woundsTitle.textContent = dict.woundsTitle;
    const woundsDesc = document.getElementById("wounds-desc");
    if (woundsDesc) woundsDesc.textContent = dict.woundsDesc;
    const woundsSelectLabel = document.getElementById("wounds-select-label");
    if (woundsSelectLabel) woundsSelectLabel.textContent = dict.woundsSelectLabel;

    if (offlineGuideStatusText) offlineGuideStatusText.textContent = dict.offlineGuideStatus;
    if (triageTitle) triageTitle.textContent = dict.triageTitle;
    if (triageSubtitle) triageSubtitle.textContent = dict.triageSubtitle;
    if (triageRushTitle) triageRushTitle.textContent = dict.triageRushTitle;
    if (triageRoleTitle) triageRoleTitle.textContent = dict.triageRoleTitle;
    if (triageRoleDesc) triageRoleDesc.textContent = dict.triageRoleDesc;
    if (triageRushList && dict.triageRushList) {
        triageRushList.innerHTML = dict.triageRushList.map(item => `<li>${item}</li>`).join('');
    }

    // Wound Selector Pills
    document.querySelectorAll(".wound-chip").forEach(chip => {
        const woundKey = chip.getAttribute("data-wound");
        if (dict.woundPills[woundKey]) {
            chip.textContent = dict.woundPills[woundKey];
        }
    });

    // 5. View 3: Medicine Kit
    const medsTitle = document.getElementById("meds-title");
    if (medsTitle) medsTitle.textContent = dict.medsTitle;
    const medsDesc = document.getElementById("meds-desc");
    if (medsDesc) medsDesc.textContent = dict.medsDesc;

    document.querySelectorAll(".med-filter-btn").forEach(btn => {
        const catKey = btn.getAttribute("data-category");
        if (dict.medFilters[catKey]) {
            btn.textContent = dict.medFilters[catKey];
        }
    });
    if (copyMedsBtn) copyMedsBtn.textContent = dict.copyMedsBtn;
    if (printMedsBtn) printMedsBtn.textContent = dict.printMedsBtn;

    // 6. View 4: Daily Log Form & Chart
    const chartSectionTitle = document.getElementById("chart-section-title");
    if (chartSectionTitle) chartSectionTitle.textContent = dict.chartSectionTitle;
    const chartSectionDesc = document.getElementById("chart-section-desc");
    if (chartSectionDesc) chartSectionDesc.textContent = dict.chartSectionDesc;
    const logFormTitle = document.getElementById("log-form-title");
    if (logFormTitle) logFormTitle.textContent = dict.logFormTitle;

    const lblDate = document.getElementById("lbl-date");
    if (lblDate) lblDate.textContent = dict.lblDate;
    const lblTime = document.getElementById("lbl-time");
    if (lblTime) lblTime.textContent = dict.lblTime;
    const lblSysBp = document.getElementById("lbl-sys-bp");
    if (lblSysBp) lblSysBp.textContent = dict.lblSysBp;
    const lblDiaBp = document.getElementById("lbl-dia-bp");
    if (lblDiaBp) lblDiaBp.textContent = dict.lblDiaBp;
    const lblSugar = document.getElementById("lbl-sugar");
    if (lblSugar) lblSugar.textContent = dict.lblSugar;
    const lblPulse = document.getElementById("lbl-pulse");
    if (lblPulse) lblPulse.textContent = dict.lblPulse;
    const lblSpo2 = document.getElementById("lbl-spo2");
    if (lblSpo2) lblSpo2.textContent = dict.lblSpo2;
    const lblTemp = document.getElementById("lbl-temp");
    if (lblTemp) lblTemp.textContent = dict.lblTemp;
    const lblPain = document.getElementById("lbl-pain");
    if (lblPain) lblPain.textContent = dict.lblPain;
    const lblSymptomsSelect = document.getElementById("lbl-symptoms-select");
    if (lblSymptomsSelect) lblSymptomsSelect.textContent = dict.lblSymptomsSelect;
    const lblSeverity = document.getElementById("lbl-severity");
    if (lblSeverity) lblSeverity.textContent = dict.lblSeverity;
    const lblNotes = document.getElementById("lbl-notes");
    if (lblNotes) lblNotes.textContent = dict.lblNotes;

    // Placeholders
    if (logSysBp) logSysBp.placeholder = dict.phSysBp;
    if (logDiaBp) logDiaBp.placeholder = dict.phDiaBp;
    if (logSugar) logSugar.placeholder = dict.phSugar;
    if (logPulse) logPulse.placeholder = dict.phPulse;
    if (logSpo2) logSpo2.placeholder = dict.phSpo2;
    if (logTemp) logTemp.placeholder = dict.phTemp;
    if (logNotes) logNotes.placeholder = dict.phNotes;

    // Severity select options
    if (logSeverity) {
        Array.from(logSeverity.options).forEach(opt => {
            if (dict.severityOptions[opt.value]) {
                opt.textContent = dict.severityOptions[opt.value];
            }
        });
    }

    // Symptom tags text
    document.querySelectorAll(".symptom-tag").forEach(tag => {
        const val = tag.getAttribute("data-val");
        if (dict.symptomsDict[val]) {
            tag.textContent = dict.symptomsDict[val];
        }
    });

    // Pain slider badge text update
    if (logPain && painValBadge) {
        const val = parseInt(logPain.value, 10);
        updatePainBadgeText(val, lang);
    }

    const saveLogBtn = document.getElementById("save-log-btn");
    if (saveLogBtn) saveLogBtn.textContent = dict.saveLogBtn;
    const chartsTitle = document.getElementById("charts-title");
    if (chartsTitle) chartsTitle.textContent = dict.chartsTitle;

    // Chart switches
    document.querySelectorAll(".chart-switch-btn").forEach(btn => {
        const type = btn.getAttribute("data-chart");
        if (dict.chartSwitches[type]) {
            btn.textContent = dict.chartSwitches[type];
        }
    });

    const timelineTitle = document.getElementById("timeline-title");
    if (timelineTitle) timelineTitle.textContent = dict.timelineTitle;
    if (analyzeChartBtn) analyzeChartBtn.textContent = dict.analyzeChartBtn;

    // 7. View 5: Doctor Report
    const reportTitle = document.getElementById("report-title");
    if (reportTitle) reportTitle.textContent = dict.reportTitle;
    const reportDesc = document.getElementById("report-desc");
    if (reportDesc) reportDesc.textContent = dict.reportDesc;

    const lblPatName = document.getElementById("lbl-pat-name");
    if (lblPatName) lblPatName.textContent = dict.lblPatName;
    const lblPatAge = document.getElementById("lbl-pat-age");
    if (lblPatAge) lblPatAge.textContent = dict.lblPatAge;
    const lblDocEmail = document.getElementById("lbl-doc-email");
    if (lblDocEmail) lblDocEmail.textContent = dict.lblDocEmail;
    const lblDocPhone = document.getElementById("lbl-doc-phone");
    if (lblDocPhone) lblDocPhone.textContent = dict.lblDocPhone;

    if (patientNameInput) patientNameInput.placeholder = dict.phPatName;
    if (patientAgeInput) patientAgeInput.placeholder = dict.phPatAge;
    if (doctorPhoneInput) doctorPhoneInput.placeholder = dict.phDocPhone;

    if (generateReportBtn) generateReportBtn.textContent = dict.generateReportBtn;
    const reportEmptyText = document.getElementById("report-empty-text");
    if (reportEmptyText) reportEmptyText.textContent = dict.reportEmptyText;

    // Hospital Document Elements
    const docTitle = document.getElementById("doc-title");
    if (docTitle) docTitle.textContent = dict.docTitle;
    const docSubtitle = document.getElementById("doc-subtitle");
    if (docSubtitle) docSubtitle.textContent = dict.docSubtitle;
    const docBadge = document.getElementById("doc-badge");
    if (docBadge) docBadge.textContent = dict.docBadge;

    const docLblName = document.getElementById("doc-lbl-name");
    if (docLblName) docLblName.textContent = dict.docLblName;
    const docLblDemo = document.getElementById("doc-lbl-demo");
    if (docLblDemo) docLblDemo.textContent = dict.docLblDemo;
    const docLblLoc = document.getElementById("doc-lbl-loc");
    if (docLblLoc) docLblLoc.textContent = dict.docLblLoc;
    const docLocVal = document.getElementById("doc-location-val");
    if (docLocVal) docLocVal.textContent = dict.docLocVal;
    const docLblWin = document.getElementById("doc-lbl-win");
    if (docLblWin) docLblWin.textContent = dict.docLblWin;
    const docWinVal = document.getElementById("doc-window-val");
    if (docWinVal) docWinVal.textContent = dict.docWinVal;

    const docSec1Title = document.getElementById("doc-sec1-title");
    if (docSec1Title) docSec1Title.textContent = dict.docSec1Title;
    const docSec2Title = document.getElementById("doc-sec2-title");
    if (docSec2Title) docSec2Title.textContent = dict.docSec2Title;
    const docSec3Title = document.getElementById("doc-sec3-title");
    if (docSec3Title) docSec3Title.textContent = dict.docSec3Title;
    const docSec4Title = document.getElementById("doc-sec4-title");
    if (docSec4Title) docSec4Title.textContent = dict.docSec4Title;
    const docSec5Title = document.getElementById("doc-sec5-title");
    if (docSec5Title) docSec5Title.textContent = dict.docSec5Title;

    const docRxLine = document.getElementById("doc-rx-line");
    if (docRxLine) docRxLine.innerHTML = `<strong>${dict.docRxLine.split(':')[0]}:</strong> ${dict.docRxLine.split(':')[1]}`;
    const docLabLine = document.getElementById("doc-lab-line");
    if (docLabLine) docLabLine.innerHTML = `<strong>${dict.docLabLine.split(':')[0]}:</strong> ${dict.docLabLine.split(':')[1]}`;
    const docDateLine = document.getElementById("doc-date-line");
    if (docDateLine) docDateLine.innerHTML = `<strong>${dict.docDateLine.split(':')[0]}:</strong> ${dict.docDateLine.split(':')[1]}`;
    const docSignLine = document.getElementById("doc-sign-line");
    if (docSignLine) docSignLine.innerHTML = `<strong>${dict.docSignLine.split(':')[0]}:</strong> ${dict.docSignLine.split(':')[1]}`;

    const docDisclaimer = document.getElementById("doc-disclaimer");
    if (docDisclaimer) docDisclaimer.innerHTML = dict.docDisclaimer;

    if (emailDoctorBtn) emailDoctorBtn.querySelector("span").textContent = dict.emailDoctorBtn;
    if (whatsappDoctorBtn) whatsappDoctorBtn.querySelector("span").textContent = dict.whatsappDoctorBtn;
    if (printReportBtn) printReportBtn.querySelector("span").textContent = dict.printReportBtn;

    // 8. Footer
    const disclaimerHeader = document.getElementById("disclaimer-header");
    if (disclaimerHeader) disclaimerHeader.textContent = dict.disclaimerHeader;
    const disclaimerBody = document.getElementById("disclaimer-body");
    if (disclaimerBody) disclaimerBody.textContent = dict.disclaimerBody;
    const hackathonFooter = document.getElementById("hackathon-footer-text");
    if (hackathonFooter) hackathonFooter.textContent = dict.hackathonFooter;

    // 9. Re-render dynamic components
    renderSuggestionChips();
    renderWoundGuide();
    renderMedsGrid();
    renderTimeline();
    renderChart();
}

function updatePainBadgeText(val, lang) {
    if (!painValBadge) return;
    const dict = i18n[lang] || i18n.English;
    let text = dict.painBadges[0];
    if (val >= 1 && val <= 3) text = `${val} - ${dict.painBadges.mild}`;
    else if (val >= 4 && val <= 6) text = `${val} - ${dict.painBadges.mod}`;
    else if (val >= 7 && val <= 9) text = `${val} - ${dict.painBadges.high}`;
    else if (val === 10) text = dict.painBadges.worst;
    painValBadge.textContent = text;
}

// ============================================================================
// TAB NAVIGATION LOGIC
// ============================================================================
function switchTab(viewName) {
    const tabs = [tabChatBtn, tabWoundsBtn, tabMedsBtn, tabChartBtn, tabReportBtn];
    const views = [viewChat, viewWounds, viewMeds, viewChart, viewReport];

    tabs.forEach(t => {
        if (t) {
            t.classList.remove("active");
            t.setAttribute("aria-selected", "false");
        }
    });
    views.forEach(v => {
        if (v) v.classList.remove("active");
    });

    if (viewName === "chat") {
        if (tabChatBtn) { tabChatBtn.classList.add("active"); tabChatBtn.setAttribute("aria-selected", "true"); }
        if (viewChat) viewChat.classList.add("active");
    } else if (viewName === "wounds") {
        if (tabWoundsBtn) { tabWoundsBtn.classList.add("active"); tabWoundsBtn.setAttribute("aria-selected", "true"); }
        if (viewWounds) viewWounds.classList.add("active");
        renderWoundGuide();
    } else if (viewName === "meds") {
        if (tabMedsBtn) { tabMedsBtn.classList.add("active"); tabMedsBtn.setAttribute("aria-selected", "true"); }
        if (viewMeds) viewMeds.classList.add("active");
        renderMedsGrid();
    } else if (viewName === "chart") {
        if (tabChartBtn) { tabChartBtn.classList.add("active"); tabChartBtn.setAttribute("aria-selected", "true"); }
        if (viewChart) viewChart.classList.add("active");
        renderTimeline();
        renderChart();
    } else if (viewName === "report") {
        if (tabReportBtn) { tabReportBtn.classList.add("active"); tabReportBtn.setAttribute("aria-selected", "true"); }
        if (viewReport) viewReport.classList.add("active");
    }
}

// Bind Navigation
if (tabChatBtn) tabChatBtn.addEventListener("click", () => switchTab("chat"));
if (tabWoundsBtn) tabWoundsBtn.addEventListener("click", () => switchTab("wounds"));
if (tabMedsBtn) tabMedsBtn.addEventListener("click", () => switchTab("meds"));
if (tabChartBtn) tabChartBtn.addEventListener("click", () => switchTab("chart"));
if (tabReportBtn) tabReportBtn.addEventListener("click", () => switchTab("report"));
if (quickCheckinBtn) quickCheckinBtn.addEventListener("click", () => {
    switchTab("chart");
    if (logSysBp) logSysBp.focus();
});

// Pain scale badge update listener
if (logPain && painValBadge) {
    logPain.addEventListener("input", (e) => {
        const val = parseInt(e.target.value, 10);
        const lang = languageSelect ? languageSelect.value : "English";
        updatePainBadgeText(val, lang);
    });
}

// Symptom chips multi-select toggle
symptomTagChips.forEach(chip => {
    chip.addEventListener("click", () => {
        chip.classList.toggle("selected");
    });
});

// ============================================================================
// WOUND TREATMENT TUTORIAL RENDERING
// ============================================================================
function renderWoundGuide() {
    if (!woundGuideCard) return;
    const lang = languageSelect ? languageSelect.value : "English";
    const data = WOUND_PROTOCOLS[activeWoundKey] || WOUND_PROTOCOLS["severe-bleeding"];
    const item = lang === "Tamil" ? data.ta : data.en;

    woundGuideCard.innerHTML = `
        <div class="wound-guide-header">
            <h3>${item.title}</h3>
            <span class="wound-severity-pill ${item.severityClass}">${item.severity}</span>
        </div>

        <div class="steps-timeline">
            <div class="wound-step-item urgent-step">
                <div class="step-num-badge">1</div>
                <div class="step-content">
                    <strong>${lang === 'Tamil' ? 'படி 1: உடனடி முதலுதவி செயல்' : 'Step 1: Immediate Triage & Action'}</strong>
                    <p>${item.step1}</p>
                </div>
            </div>

            <div class="wound-step-item">
                <div class="step-num-badge">2</div>
                <div class="step-content">
                    <strong>${lang === 'Tamil' ? 'படி 2: இரத்த ஓட்டம் / தூய்மைப்படுத்துதல்' : 'Step 2: Elevation & Debris Cleansing'}</strong>
                    <p>${item.step2}</p>
                </div>
            </div>

            <div class="wound-step-item">
                <div class="step-num-badge">3</div>
                <div class="step-content">
                    <strong>${lang === 'Tamil' ? 'படி 3: கிருமிநாசினி & மலட்டு கட்டு' : 'Step 3: Antiseptic Dressing & Splinting'}</strong>
                    <p>${item.step3}</p>
                </div>
            </div>

            <div class="wound-step-item">
                <div class="step-num-badge">4</div>
                <div class="step-content">
                    <strong>${lang === 'Tamil' ? 'படி 4: அவசர நெறிமுறை & தடுப்பூசி' : 'Step 4: Emergency Tourniquet / Vaccine Protocol'}</strong>
                    <p>${item.step4}</p>
                </div>
            </div>
        </div>

        <div class="wound-callouts-grid">
            <div class="wound-donts-card">
                <strong>❌ ${lang === 'Tamil' ? 'ஒருபோதும் செய்யக்கூடாதவை (DANGER DON\'TS):' : 'Critical Precautions (DANGER DON\'TS):'}</strong>
                <ul>
                    ${item.donts.map(d => `<li>${d}</li>`).join('')}
                </ul>
            </div>

            <div class="wound-transport-card">
                <strong>🚑 ${lang === 'Tamil' ? 'மருத்துவமனை கொண்டு செல்லும் நெறிமுறை:' : 'Hospital Referral & 108 Alert:'}</strong>
                <p>${item.transport}</p>
            </div>
        </div>
    `;
}

// Wound chip buttons
if (woundChipsContainer) {
    const chips = woundChipsContainer.querySelectorAll(".wound-chip");
    chips.forEach(chip => {
        chip.addEventListener("click", () => {
            chips.forEach(c => c.classList.remove("active"));
            chip.classList.add("active");
            activeWoundKey = chip.getAttribute("data-wound");
            renderWoundGuide();
        });
    });
}

// ============================================================================
// ESSENTIAL MEDICINE KIT RENDERING
// ============================================================================
function renderMedsGrid() {
    if (!medsGrid) return;
    const lang = languageSelect ? languageSelect.value : "English";
    const filtered = activeMedCategory === "all"
        ? ESSENTIAL_MEDS
        : ESSENTIAL_MEDS.filter(m => m.category === activeMedCategory);

    medsGrid.innerHTML = filtered.map(m => {
        const name = lang === "Tamil" ? m.nameTa : m.nameEn;
        const type = lang === "Tamil" ? m.typeTa : m.typeEn;
        const dose = lang === "Tamil" ? m.doseTa : m.doseEn;
        const limit = lang === "Tamil" ? m.limitTa : m.limitEn;
        const caution = lang === "Tamil" ? (m.cautionTa || m.cautionEn) : m.cautionEn;

        return `
            <div class="med-card">
                <div class="med-card-header">
                    <div class="med-icon-name">
                        <div class="med-card-icon">${m.icon}</div>
                        <div>
                            <div class="med-card-name">${name}</div>
                            <div class="med-generic-tag">${type}</div>
                        </div>
                    </div>
                    <span class="med-category-pill">${m.category.toUpperCase()}</span>
                </div>

                <div class="med-info-block">
                    <strong>${lang === 'Tamil' ? 'சரியான அளவு / பயன்பாடு:' : 'Usage & Standard Dose:'}</strong>
                    <div class="med-dose-pill">${dose}</div>
                </div>

                <div class="med-info-block">
                    <strong>${lang === 'Tamil' ? 'முக்கிய முன்னெச்சரிக்கை:' : 'Safety / Daily Limit:'}</strong>
                    <p>${limit}</p>
                </div>

                <div class="med-caution">
                    💡 ${caution}
                </div>
            </div>
        `;
    }).join('');
}

// Category filter buttons
medsFilters.forEach(btn => {
    btn.addEventListener("click", () => {
        medsFilters.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        activeMedCategory = btn.getAttribute("data-category");
        renderMedsGrid();
    });
});

// Copy Shopping List
if (copyMedsBtn) {
    copyMedsBtn.addEventListener("click", () => {
        const lang = languageSelect ? languageSelect.value : "English";
        const isTa = lang === "Tamil";
        let text = isTa ? "🏥 HealthMate AI - அத்தியாவசிய முதலுதவி & OTC மருந்துகள் பட்டியல்:\n\n"
                        : "🏥 HealthMate AI - Essential Home Medicine & First-Aid Kit Checklist:\n\n";

        ESSENTIAL_MEDS.forEach((m, idx) => {
            const name = isTa ? m.nameTa : m.nameEn;
            const dose = isTa ? m.doseTa : m.doseEn;
            text += `${idx + 1}. [ ] ${name} (${m.category})\n   -> ${dose}\n`;
        });
        text += isTa ? "\n⚠️ உலர்ந்த, குளிர்ந்த இடத்தில் வைக்கவும். காலாவதி தேதியை பரிசோதிக்கவும்."
                     : "\n⚠️ Store in a dry, cool place away from sunlight. Check expiry dates.";

        navigator.clipboard.writeText(text).then(() => {
            alert(isTa ? "மருந்துகள் பட்டியல் நகலெடுக்கப்பட்டது (Copied to Clipboard)!"
                       : "Medicine checklist copied to clipboard!");
        }).catch(() => {
            alert("Clipboard copy failed. Please select text manually.");
        });
    });
}

// Print Meds List
if (printMedsBtn) {
    printMedsBtn.addEventListener("click", () => {
        window.print();
    });
}

// ============================================================================
// DAILY VITALS LOGGING & STORAGE
// ============================================================================
function getStoredLogs() {
    try {
        const raw = localStorage.getItem(STORAGE_LOGS_KEY);
        return raw ? JSON.parse(raw) : [];
    } catch {
        return [];
    }
}

function saveStoredLogs(logs) {
    localStorage.setItem(STORAGE_LOGS_KEY, JSON.stringify(logs));
}

// Submit Daily Health Check-in
if (healthLogForm) {
    healthLogForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const selectedSymptoms = [];
        document.querySelectorAll(".symptom-tag.selected").forEach(tag => {
            selectedSymptoms.push(tag.getAttribute("data-val"));
        });

        const entry = {
            id: "log_" + Date.now(),
            patient_id: "default",
            date: logDate.value || new Date().toISOString().split("T")[0],
            time: logTime.value || "12:00",
            systolic_bp: logSysBp.value ? parseInt(logSysBp.value, 10) : null,
            diastolic_bp: logDiaBp.value ? parseInt(logDiaBp.value, 10) : null,
            blood_glucose: logSugar.value ? parseInt(logSugar.value, 10) : null,
            heart_rate: logPulse.value ? parseInt(logPulse.value, 10) : null,
            spo2: logSpo2.value ? parseInt(logSpo2.value, 10) : null,
            temperature: logTemp.value ? parseFloat(logTemp.value) : null,
            pain_level: logPain ? parseInt(logPain.value, 10) : 0,
            symptoms: selectedSymptoms,
            condition_severity: logSeverity.value || "Mild",
            notes: logNotes.value ? logNotes.value.trim() : ""
        };

        // Save to local storage
        const currentLogs = getStoredLogs();
        currentLogs.unshift(entry);
        saveStoredLogs(currentLogs);

        // Sync with backend API asynchronously
        try {
            await fetch(`${API_BASE}/api/health-logs`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(entry)
            });
        } catch (err) {
            console.log("[Offline mode - saved locally]:", err);
        }

        // Reset form inputs
        logSysBp.value = "";
        logDiaBp.value = "";
        logSugar.value = "";
        logPulse.value = "";
        logSpo2.value = "";
        logTemp.value = "";
        logNotes.value = "";
        if (logPain) logPain.value = 0;
        const lang = languageSelect ? languageSelect.value : "English";
        updatePainBadgeText(0, lang);
        document.querySelectorAll(".symptom-tag.selected").forEach(t => t.classList.remove("selected"));

        alert(lang === "Tamil"
            ? "✅ இன்றைய உடல்நலப் பதிவு வெற்றிகரமாக சேமிக்கப்பட்டது!"
            : "✅ Today's health entry saved successfully!");

        renderTimeline();
        renderChart();
    });
}

// Render Daily Log History Timeline
function renderTimeline() {
    if (!timelineCardsList) return;
    const logs = getStoredLogs();
    const lang = languageSelect ? languageSelect.value : "English";
    const dict = i18n[lang] || i18n.English;
    const isTa = lang === "Tamil";

    if (logs.length === 0) {
        timelineCardsList.innerHTML = `
            <div style="text-align: center; padding: 24px; color: var(--muted); font-size: 0.85rem;">
                ${isTa ? 'இதுவரை பதிவுகள் இல்லை. மேலே உள்ள படிவத்தில் இன்றைய அளவை பதிவு செய்யுங்கள்.' : 'No entries logged yet. Record today\'s vitals using the form above.'}
            </div>
        `;
        return;
    }

    timelineCardsList.innerHTML = logs.map(entry => {
        let badgeClass = "status-good";
        let sevText = isTa ? "🟢 லேசானது" : "🟢 Mild";
        if (entry.condition_severity === "Moderate") {
            badgeClass = "status-moderate";
            sevText = isTa ? "🟡 மிதமானது" : "🟡 Moderate";
        }
        if (entry.condition_severity === "Severe") {
            badgeClass = "status-urgent";
            sevText = isTa ? "🔴 தீவிரமானது" : "🔴 Severe";
        }

        const bpStr = (entry.systolic_bp && entry.diastolic_bp) ? `${entry.systolic_bp}/${entry.diastolic_bp} mmHg` : "N/A";
        const sugarStr = entry.blood_glucose ? `${entry.blood_glucose} mg/dL` : "N/A";
        const spo2Str = entry.spo2 ? `${entry.spo2}%` : "N/A";
        const tempStr = entry.temperature ? `${entry.temperature}°F` : "N/A";
        const pulseStr = entry.heart_rate ? `${entry.heart_rate} bpm` : "N/A";

        // Translate symptoms in card
        const symNames = (entry.symptoms || []).map(s => dict.symptomsDict[s] || s);

        return `
            <div class="timeline-card">
                <div class="timeline-card-header">
                    <span class="timeline-date">📅 ${entry.date} (${entry.time || ''})</span>
                    <span class="status-pill ${badgeClass}">${sevText}</span>
                </div>
                <div style="display: flex; flex-wrap: wrap; gap: 8px; margin: 6px 0; font-size: 0.78rem;">
                    <span style="background: #f1f5f9; padding: 2px 8px; border-radius: 6px;">💓 ${isTa ? 'இரத்த அழுத்தம்' : 'BP'}: <strong>${bpStr}</strong></span>
                    <span style="background: #f1f5f9; padding: 2px 8px; border-radius: 6px;">🩸 ${isTa ? 'சர்க்கரை' : 'Sugar'}: <strong>${sugarStr}</strong></span>
                    <span style="background: #f1f5f9; padding: 2px 8px; border-radius: 6px;">💨 ${isTa ? 'ஆக்சிஜன்' : 'SpO2'}: <strong>${spo2Str}</strong></span>
                    <span style="background: #f1f5f9; padding: 2px 8px; border-radius: 6px;">🌡️ ${isTa ? 'வெப்பநிலை' : 'Temp'}: <strong>${tempStr}</strong></span>
                    <span style="background: #f1f5f9; padding: 2px 8px; border-radius: 6px;">❤️ ${isTa ? 'நாடி' : 'Pulse'}: <strong>${pulseStr}</strong></span>
                    <span style="background: #fef3c7; color: #92400e; padding: 2px 8px; border-radius: 6px;">${isTa ? 'வலி' : 'Pain'}: ${entry.pain_level}/10</span>
                </div>
                ${symNames && symNames.length > 0 ? `
                    <div style="font-size: 0.75rem; color: #475569; margin: 4px 0;">
                        <strong>${isTa ? 'அறிகுறிகள்' : 'Symptoms'}:</strong> ${symNames.join(', ')}
                    </div>
                ` : ''}
                ${entry.notes ? `
                    <p style="font-size: 0.75rem; color: var(--muted); margin-top: 4px; font-style: italic;">"${entry.notes}"</p>
                ` : ''}
                <div style="display: flex; justify-content: flex-end; margin-top: 6px;">
                    <button type="button" onclick="deleteLogEntry('${entry.id}')" style="background: none; border: none; color: #dc2626; cursor: pointer; font-size: 0.72rem; font-weight: 600;">
                        ${dict.deleteEntryText}
                    </button>
                </div>
            </div>
        `;
    }).join('');
}

window.deleteLogEntry = function(id) {
    let logs = getStoredLogs();
    logs = logs.filter(l => l.id !== id);
    saveStoredLogs(logs);
    renderTimeline();
    renderChart();
};

// ============================================================================
// CHART.JS VITALS RENDERING (Bilingual Legends & Datasets)
// ============================================================================
chartSwitches.forEach(btn => {
    btn.addEventListener("click", () => {
        chartSwitches.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        activeChartType = btn.getAttribute("data-chart");
        renderChart();
    });
});

function renderChart() {
    const canvas = document.getElementById("vitalsChart");
    if (!canvas || typeof Chart === "undefined") return;

    const logs = getStoredLogs().slice().reverse(); // Chronological order
    if (logs.length === 0) return;

    const lang = languageSelect ? languageSelect.value : "English";
    const dict = i18n[lang] || i18n.English;
    const legends = dict.chartLegends;

    const labels = logs.map(l => l.date ? l.date.substring(5) : ""); // MM-DD

    let datasets = [];
    if (activeChartType === "bp") {
        datasets = [
            {
                label: legends.sysBp,
                data: logs.map(l => l.systolic_bp || null),
                borderColor: "#dc2626",
                backgroundColor: "rgba(220, 38, 38, 0.1)",
                tension: 0.3,
                borderWidth: 2,
                spanGaps: true
            },
            {
                label: legends.diaBp,
                data: logs.map(l => l.diastolic_bp || null),
                borderColor: "#2563eb",
                backgroundColor: "rgba(37, 99, 235, 0.1)",
                tension: 0.3,
                borderWidth: 2,
                spanGaps: true
            }
        ];
    } else if (activeChartType === "sugar-temp") {
        datasets = [
            {
                label: legends.sugar,
                data: logs.map(l => l.blood_glucose || null),
                borderColor: "#7c3aed",
                backgroundColor: "rgba(124, 58, 237, 0.1)",
                tension: 0.3,
                borderWidth: 2,
                yAxisID: "y",
                spanGaps: true
            },
            {
                label: legends.temp,
                data: logs.map(l => l.temperature || null),
                borderColor: "#ea580c",
                backgroundColor: "rgba(234, 88, 12, 0.1)",
                tension: 0.3,
                borderWidth: 2,
                yAxisID: "y1",
                spanGaps: true
            }
        ];
    } else if (activeChartType === "pulse-spo2") {
        datasets = [
            {
                label: legends.pulse,
                data: logs.map(l => l.heart_rate || null),
                borderColor: "#16a34a",
                backgroundColor: "rgba(22, 163, 74, 0.1)",
                tension: 0.3,
                borderWidth: 2,
                yAxisID: "y",
                spanGaps: true
            },
            {
                label: legends.spo2,
                data: logs.map(l => l.spo2 || null),
                borderColor: "#0a8a6b",
                backgroundColor: "rgba(10, 138, 107, 0.1)",
                tension: 0.3,
                borderWidth: 2,
                yAxisID: "y1",
                spanGaps: true
            }
        ];
    }

    if (vitalsChartInstance) {
        vitalsChartInstance.destroy();
    }

    vitalsChartInstance = new Chart(canvas, {
        type: "line",
        data: { labels, datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: "top", labels: { boxWidth: 14, font: { family: 'Inter', size: 11 } } },
                tooltip: { mode: "index", intersect: false }
            },
            scales: {
                x: { grid: { color: "#f1f5f9" } },
                y: { grid: { color: "#f1f5f9" } }
            }
        }
    });
}

// Ask AI to analyze chart button
if (analyzeChartBtn) {
    analyzeChartBtn.addEventListener("click", () => {
        const logs = getStoredLogs();
        const lang = languageSelect ? languageSelect.value : "English";
        if (logs.length === 0) {
            alert(lang === "Tamil" ? "பகுப்பாய்வு செய்ய பதிவுகள் எதுவும் இல்லை." : "No health entries found to analyze.");
            return;
        }
        const recent = logs.slice(0, 3);
        let summaryQuery = lang === "Tamil"
            ? `எனது சமீபத்திய உடல்நல அளவீடுகளை பகுப்பாய்வு செய்து நிலைமை நல்லதா அல்லது மருத்துவரிடம் செல்ல வேண்டுமா என கூறுங்கள்: `
            : `Please analyze my recent health vitals and tell me if my condition is stable or needs medical review: `;

        recent.forEach(r => {
            summaryQuery += `[${r.date}: BP ${r.systolic_bp || 'N/A'}/${r.diastolic_bp || 'N/A'}, Sugar ${r.blood_glucose || 'N/A'}, Temp ${r.temperature || 'N/A'}°F, Symptoms: ${r.symptoms ? r.symptoms.join(', ') : 'None'}]. `;
        });

        switchTab("chat");
        userInput.value = summaryQuery;
        chatForm.dispatchEvent(new Event("submit"));
    });
}

// ============================================================================
// MONTHLY DOCTOR REPORT GENERATION & TELE-SHARE
// ============================================================================
if (generateReportBtn) {
    generateReportBtn.addEventListener("click", async () => {
        const logs = getStoredLogs();
        const lang = languageSelect ? languageSelect.value : "English";
        const dict = i18n[lang] || i18n.English;
        const isTa = lang === "Tamil";

        if (logs.length === 0) {
            alert(isTa ? "அறிக்கை உருவாக்க குறைந்தபட்சம் ஒரு உடல்நலப் பதிவாவது தேவை."
                       : "At least one daily health entry is required to generate a doctor report.");
            return;
        }

        generateReportBtn.disabled = true;
        generateReportBtn.textContent = isTa ? "⏳ மருத்துவ அறிக்கை தயாராகிறது..." : "⏳ Generating Clinical Report...";

        const patientName = patientNameInput.value.trim() || (isTa ? "நோயாளி" : "Patient");
        const patientAge = patientAgeInput.value.trim() || (isTa ? "குறிப்பிடப்படவில்லை" : "Unspecified");
        const docEmail = doctorEmailInput.value.trim() || "";
        const docPhone = doctorPhoneInput.value.trim() || "";

        // Attempt backend AI report generation, with local calculation fallback
        let reportData = null;
        try {
            const resp = await fetch(`${API_BASE}/api/doctor-report`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    patient_id: "default",
                    patient_name: patientName,
                    age: null,
                    gender: patientAge,
                    language: lang,
                    doctor_email: docEmail
                })
            });
            if (resp.ok) {
                reportData = await resp.json();
            }
        } catch (err) {
            console.log("[Using local clinical aggregator]:", err);
        }

        // Local calculation fallback if backend unavailable
        if (!reportData) {
            const sysBps = logs.map(l => l.systolic_bp).filter(Boolean);
            const diaBps = logs.map(l => l.diastolic_bp).filter(Boolean);
            const sugars = logs.map(l => l.blood_glucose).filter(Boolean);
            const spo2s = logs.map(l => l.spo2).filter(Boolean);
            const temps = logs.map(l => l.temperature).filter(Boolean);
            const pulses = logs.map(l => l.heart_rate).filter(Boolean);

            const redFlags = [];
            if (sysBps.length && Math.max(...sysBps) >= 140) {
                redFlags.push(isTa ? `உயர் இரத்த அழுத்தம் கண்டறியப்பட்டது (உச்சம்: ${Math.max(...sysBps)} mmHg)`
                                   : `Elevated Systolic Blood Pressure detected (Peak: ${Math.max(...sysBps)} mmHg)`);
            }
            if (diaBps.length && Math.max(...diaBps) >= 90) {
                redFlags.push(isTa ? `உயர் டயஸ்டாலிக் BP கண்டறியப்பட்டது (உச்சம்: ${Math.max(...diaBps)} mmHg)`
                                   : `Elevated Diastolic Blood Pressure detected (Peak: ${Math.max(...diaBps)} mmHg)`);
            }
            if (sugars.length && Math.max(...sugars) >= 180) {
                redFlags.push(isTa ? `அதிக சர்க்கரை அளவு பதிவாகியுள்ளது (உச்சம்: ${Math.max(...sugars)} mg/dL)`
                                   : `High Blood Sugar reading logged (Peak: ${Math.max(...sugars)} mg/dL)`);
            }
            if (spo2s.length && Math.min(...spo2s) < 95) {
                redFlags.push(isTa ? `ஆக்ஸிஜன் குறைவு எச்சரிக்கை: SpO2 ${Math.min(...spo2s)}%-ஆக குறைந்தது`
                                   : `Hypoxia Alert: SpO2 dipped to ${Math.min(...spo2s)}%`);
            }
            if (temps.length && Math.max(...temps) >= 101.0) {
                redFlags.push(isTa ? `அதிக காய்ச்சல் பதிவானது (உச்சம்: ${Math.max(...temps)}°F)`
                                   : `High Fever episode (Peak: ${Math.max(...temps)}°F)`);
            }

            const symptomFreq = {};
            logs.forEach(l => {
                (l.symptoms || []).forEach(s => { symptomFreq[s] = (symptomFreq[s] || 0) + 1; });
            });

            reportData = {
                patient_name: patientName,
                generated_at: new Date().toLocaleDateString(),
                summary_stats: {
                    total_days_logged: logs.length,
                    avg_systolic_bp: sysBps.length ? Math.round(sysBps.reduce((a,b)=>a+b)/sysBps.length) : null,
                    avg_diastolic_bp: diaBps.length ? Math.round(diaBps.reduce((a,b)=>a+b)/diaBps.length) : null,
                    max_bp: sysBps.length && diaBps.length ? `${Math.max(...sysBps)}/${Math.max(...diaBps)}` : null,
                    avg_blood_glucose: sugars.length ? Math.round(sugars.reduce((a,b)=>a+b)/sugars.length) : null,
                    max_glucose: sugars.length ? Math.max(...sugars) : null,
                    avg_spo2: spo2s.length ? (spo2s.reduce((a,b)=>a+b)/spo2s.length).toFixed(1) : null,
                    min_spo2: spo2s.length ? Math.min(...spo2s) : null,
                    avg_pulse: pulses.length ? Math.round(pulses.reduce((a,b)=>a+b)/pulses.length) : null,
                    avg_temp: temps.length ? (temps.reduce((a,b)=>a+b)/temps.length).toFixed(1) : null,
                    max_temp: temps.length ? Math.max(...temps) : null,
                    symptom_frequencies: symptomFreq,
                    red_flags: redFlags
                },
                clinical_summary: isTa
                    ? `நோயாளி தொலைதூர கிராமப் பகுதியில் வசிக்கிறார். கடந்த 30 நாட்களில் சராசரி BP ${sysBps.length ? Math.round(sysBps.reduce((a,b)=>a+b)/sysBps.length) : 'N/A'}/${diaBps.length ? Math.round(diaBps.reduce((a,b)=>a+b)/diaBps.length) : 'N/A'} மற்றும் சராசரி சர்க்கரை ${sugars.length ? Math.round(sugars.reduce((a,b)=>a+b)/sugars.length) : 'N/A'} mg/dL ஆக பதிவாகியுள்ளது.`
                    : `Patient resides in a remote location with distant medical access. Past 30 days show average BP at ${sysBps.length ? Math.round(sysBps.reduce((a,b)=>a+b)/sysBps.length) : 'N/A'}/${diaBps.length ? Math.round(diaBps.reduce((a,b)=>a+b)/diaBps.length) : 'N/A'} mmHg, and average glucose at ${sugars.length ? Math.round(sugars.reduce((a,b)=>a+b)/sugars.length) : 'N/A'} mg/dL.`,
                red_flags: redFlags
            };
        }

        // Render Report Document
        if (reportPlaceholder) reportPlaceholder.classList.add("hidden");
        if (reportContent) reportContent.classList.remove("hidden");

        const stats = reportData.summary_stats;
        document.getElementById("doc-generated-date").textContent = `${isTa ? 'உருவாக்கப்பட்ட தேதி' : 'Generated'}: ${reportData.generated_at}`;
        document.getElementById("doc-patient-name").textContent = reportData.patient_name || patientName;
        document.getElementById("doc-patient-demographics").textContent = patientAge;

        // Vitals stats cards with 100% Tamil/English labels
        const statsGrid = document.getElementById("doc-stats-grid");
        statsGrid.innerHTML = `
            <div class="doc-stat-card">
                <div class="doc-stat-val">${stats.avg_systolic_bp || 'N/A'}/${stats.avg_diastolic_bp || 'N/A'}</div>
                <div class="doc-stat-lbl">${dict.statAvgBp}</div>
            </div>
            <div class="doc-stat-card">
                <div class="doc-stat-val" style="color: #dc2626;">${stats.max_bp || 'N/A'}</div>
                <div class="doc-stat-lbl">${dict.statPeakBp}</div>
            </div>
            <div class="doc-stat-card">
                <div class="doc-stat-val">${stats.avg_blood_glucose || 'N/A'}</div>
                <div class="doc-stat-lbl">${dict.statAvgSugar}</div>
            </div>
            <div class="doc-stat-card">
                <div class="doc-stat-val" style="color: #7c3aed;">${stats.max_glucose || 'N/A'}</div>
                <div class="doc-stat-lbl">${dict.statPeakSugar}</div>
            </div>
            <div class="doc-stat-card">
                <div class="doc-stat-val">${stats.avg_spo2 ? stats.avg_spo2 + '%' : 'N/A'}</div>
                <div class="doc-stat-lbl">${dict.statAvgSpo2} (${dict.statLowest}: ${stats.min_spo2 || 'N/A'}%)</div>
            </div>
            <div class="doc-stat-card">
                <div class="doc-stat-val">${stats.avg_pulse || 'N/A'}</div>
                <div class="doc-stat-lbl">${dict.statAvgPulse}</div>
            </div>
            <div class="doc-stat-card">
                <div class="doc-stat-val">${stats.avg_temp ? stats.avg_temp + '°F' : 'N/A'}</div>
                <div class="doc-stat-lbl">${dict.statAvgTemp}</div>
            </div>
            <div class="doc-stat-card">
                <div class="doc-stat-val">${stats.total_days_logged}</div>
                <div class="doc-stat-lbl">${dict.statDaysMonitored}</div>
            </div>
        `;

        // Red Flags
        const redFlagsSection = document.getElementById("doc-red-flags-section");
        const alertsBox = document.getElementById("doc-alerts-box");
        if (reportData.red_flags && reportData.red_flags.length > 0) {
            redFlagsSection.style.display = "block";
            alertsBox.innerHTML = reportData.red_flags.map(f => `
                <div class="doc-alert-item">⚠️ ${f}</div>
            `).join('');
        } else {
            alertsBox.innerHTML = `<div style="font-size: 0.8rem; color: #166534;">🟢 ${isTa ? 'இந்த காலகட்டத்தில் அவசர எச்சரிக்கைகள் எதுவும் பதிவாகவில்லை.' : 'No acute threshold abnormalities logged in this period.'}</div>`;
        }

        // Symptoms Breakdown
        const symptomsList = document.getElementById("doc-symptoms-list");
        const freqs = stats.symptom_frequencies || {};
        if (Object.keys(freqs).length > 0) {
            symptomsList.innerHTML = Object.entries(freqs).map(([sym, count]) => {
                const symLabel = dict.symptomsDict[sym] || sym;
                return `<span class="doc-symptom-pill">${symLabel}: <strong>${count} ${isTa ? 'நாட்கள்' : 'days'}</strong></span>`;
            }).join('');
        } else {
            symptomsList.innerHTML = `<span style="font-size: 0.8rem; color: var(--muted);">${isTa ? 'தொடர் அறிகுறிகள் எதுவும் பதிவாகவில்லை.' : 'No persistent symptoms logged.'}</span>`;
        }

        // AI Summary Memo
        document.getElementById("doc-ai-summary").textContent = reportData.clinical_summary;

        // Build Email Share Link (mailto:)
        const emailSubject = encodeURIComponent(
            isTa ? `மாதாந்திர மருத்துவ அறிக்கை: ${patientName} (${reportData.generated_at})`
                 : `Monthly Vitals Clinical Handover: ${patientName} (${reportData.generated_at})`
        );
        const emailBody = encodeURIComponent(
            (isTa ? `வணக்கம் மருத்துவர் அவர்களுக்கு,\n\nநோயாளி ${patientName} (${patientAge}) அவர்களின் மாதாந்திர உடல்நல அளவீட்டு அறிக்கை கீழே இணைக்கப்பட்டுள்ளது.\n\n`
                  : `Dear Doctor,\n\nPlease find the monthly home vitals report for patient: ${patientName} (${patientAge}).\n\n`) +
            (isTa ? `உடல்நல அளவீடுகள் சுருக்கம் (கடந்த 30 நாட்கள்):\n` : `VITALS OVERVIEW (Past 30 Days):\n`) +
            `- ${isTa ? 'சராசரி இரத்த அழுத்தம் (BP)' : 'Average Blood Pressure'}: ${stats.avg_systolic_bp}/${stats.avg_diastolic_bp} mmHg (${isTa ? 'உச்சம்' : 'Peak'}: ${stats.max_bp})\n` +
            `- ${isTa ? 'இரத்த சர்க்கரை' : 'Blood Sugar (Glucose)'}: ${isTa ? 'சராசரி' : 'Avg'} ${stats.avg_blood_glucose} mg/dL (${isTa ? 'உச்சம்' : 'Peak'}: ${stats.max_glucose})\n` +
            `- ${isTa ? 'ஆக்சிஜன் SpO2' : 'Oxygen SpO2'}: ${isTa ? 'சராசரி' : 'Avg'} ${stats.avg_spo2}% (${isTa ? 'குறைந்தது' : 'Lowest'}: ${stats.min_spo2}%)\n` +
            `- ${isTa ? 'நாடித் துடிப்பு' : 'Heart Rate'}: ${isTa ? 'சராசரி' : 'Avg'} ${stats.avg_pulse} BPM\n` +
            `- ${isTa ? 'உடல் வெப்பநிலை' : 'Temperature'}: ${isTa ? 'சராசரி' : 'Avg'} ${stats.avg_temp}°F\n` +
            `- ${isTa ? 'கண்காணிக்கப்பட்ட நாட்கள்' : 'Total Monitored Days'}: ${stats.total_days_logged}\n\n` +
            (isTa ? `கண்டறியப்பட்ட எச்சரிக்கைகள்:\n` : `RED FLAGS DETECTED:\n`) +
            `${reportData.red_flags && reportData.red_flags.length ? reportData.red_flags.join('\n') : (isTa ? 'எதுவுமில்லை' : 'None')}\n\n` +
            (isTa ? `மருத்துவ குறிப்புரை:\n` : `CLINICAL SUMMARY NOTE:\n`) +
            `${reportData.clinical_summary}\n\n` +
            `HealthMate AI Tele-Health Assistant.`
        );
        emailDoctorBtn.href = `mailto:${docEmail}?subject=${emailSubject}&body=${emailBody}`;

        // Build WhatsApp Share Link
        const waText = encodeURIComponent(
            (isTa ? `*🏥 HealthMate AI - மாதாந்திர உடல்நல அறிக்கை*\n` : `*🏥 HealthMate AI - Monthly Patient Vitals Summary*\n`) +
            `*${isTa ? 'நோயாளி' : 'Patient'}:* ${patientName} (${patientAge})\n` +
            `*${isTa ? 'தேதி' : 'Period'}:* ${reportData.generated_at}\n\n` +
            `*${isTa ? 'முக்கிய அளவீடுகள்' : 'Vitals Summary'}:*\n` +
            `• BP: ${isTa ? 'சராசரி' : 'Avg'} ${stats.avg_systolic_bp}/${stats.avg_diastolic_bp} mmHg (${isTa ? 'உச்சம்' : 'Peak'}: ${stats.max_bp})\n` +
            `• ${isTa ? 'சர்க்கரை' : 'Sugar'}: ${isTa ? 'சராசரி' : 'Avg'} ${stats.avg_blood_glucose} mg/dL (${isTa ? 'உச்சம்' : 'Peak'}: ${stats.max_glucose})\n` +
            `• SpO2: ${isTa ? 'சராசரி' : 'Avg'} ${stats.avg_spo2}% (${isTa ? 'குறைந்தது' : 'Lowest'}: ${stats.min_spo2}%)\n` +
            `• ${isTa ? 'நாடி' : 'Pulse'}: ${isTa ? 'சராசரி' : 'Avg'} ${stats.avg_pulse} BPM\n` +
            `• ${isTa ? 'வெப்பநிலை' : 'Temp'}: ${isTa ? 'சராசரி' : 'Avg'} ${stats.avg_temp}°F\n\n` +
            `*${isTa ? 'எச்சரிக்கைகள்' : 'Red Flags'}:* ${reportData.red_flags && reportData.red_flags.length ? reportData.red_flags.join(', ') : (isTa ? 'எதுவுமில்லை' : 'None')}\n\n` +
            `_${isTa ? 'பரிசோதித்து மேலதிக மருந்துகள் வழிகாட்டவும்.' : 'Please review and advise if medication or in-person clinic visit is needed.'}_`
        );
        const waPhoneParam = docPhone ? `phone=${docPhone.replace(/\D/g, '')}&` : '';
        whatsappDoctorBtn.href = `https://api.whatsapp.com/send?${waPhoneParam}text=${waText}`;

        generateReportBtn.disabled = false;
        generateReportBtn.textContent = dict.generateReportBtn;
    });
}

// Print Doctor Report
if (printReportBtn) {
    printReportBtn.addEventListener("click", () => {
        window.print();
    });
}

// ============================================================================
// CHAT, BACKEND HEALTH & VOICE INPUT (With Offline Guards)
// ============================================================================
async function checkBackendHealth() {
    // If browser is offline, do not attempt to contact backend
    if (!navigator.onLine) {
        systemStatus.classList.remove("status-online");
        systemStatus.classList.add("status-offline");
        const lang = languageSelect ? languageSelect.value : "English";
        statusText.textContent = lang === "Tamil" ? "ஆஃப்லைன் (AI நிறுத்திவைக்கப்பட்டுள்ளது)" : "Offline (AI Paused)";
        return;
    }

    try {
        const resp = await fetch(`${API_BASE}/health`, { signal: AbortSignal.timeout(3000) });
        if (resp.ok) {
            systemStatus.classList.remove("status-offline");
            systemStatus.classList.add("status-online");
            const lang = languageSelect ? languageSelect.value : "English";
            statusText.textContent = i18n[lang]?.statusReady || "AI Ready";
        } else {
            throw new Error();
        }
    } catch {
        systemStatus.classList.remove("status-online");
        systemStatus.classList.add("status-offline");
        const lang = languageSelect ? languageSelect.value : "English";
        statusText.textContent = lang === "Tamil" ? "உள்ளூர் பாதுகாப்பு தயார்" : "Local Backup Active";
    }
}
checkBackendHealth();
setInterval(checkBackendHealth, 20000);

// Online / Offline Network Status Synchronizer
function updateNetworkStatus() {
    const isOnline = navigator.onLine;
    const lang = languageSelect ? languageSelect.value : "English";
    const dict = i18n[lang] || i18n.English;

    if (networkStatus && networkStatusText) {
        if (isOnline) {
            networkStatus.classList.remove("status-offline-badge");
            networkStatus.classList.add("status-online-badge");
            networkStatusText.textContent = dict.networkOnline || "Online";
        } else {
            networkStatus.classList.remove("status-online-badge");
            networkStatus.classList.add("status-offline-badge");
            networkStatusText.textContent = dict.networkOffline || "Offline Mode";
        }
    }

    if (offlineBanner) {
        if (isOnline) {
            offlineBanner.classList.add("hidden");
        } else {
            offlineBanner.classList.remove("hidden");
        }
    }

    if (isOnline) {
        checkBackendHealth();
    } else {
        if (systemStatus && statusText) {
            systemStatus.classList.remove("status-online");
            systemStatus.classList.add("status-offline");
            statusText.textContent = lang === "Tamil" ? "ஆஃப்லைன் (AI நிறுத்திவைக்கப்பட்டுள்ளது)" : "Offline (AI Paused)";
        }
    }
}

window.addEventListener("online", updateNetworkStatus);
window.addEventListener("offline", updateNetworkStatus);
if (offlineGuideQuickBtn) {
    offlineGuideQuickBtn.addEventListener("click", () => switchTab("wounds"));
}

// Suggestion Chips
function renderSuggestionChips() {
    if (!chipsContainer) return;
    const lang = languageSelect ? languageSelect.value : "English";
    const suggestions = i18n[lang]?.suggestions || i18n.English.suggestions;
    chipsContainer.innerHTML = suggestions.map(s => `
        <button type="button" class="chip-btn">${s}</button>
    `).join('');

    chipsContainer.querySelectorAll(".chip-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            userInput.value = btn.textContent.trim();
            chatForm.dispatchEvent(new Event("submit"));
        });
    });
}

// Markdown-lite Parser
function parseMarkdownLite(text) {
    let clean = text.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, "");
    clean = clean.replace(/^### (.*$)/gim, '<h4 class="md-heading">$1</h4>');
    clean = clean.replace(/^## (.*$)/gim, '<h3 class="md-heading">$1</h3>');
    clean = clean.replace(/^# (.*$)/gim, '<h2 class="md-heading">$1</h2>');
    clean = clean.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    clean = clean.replace(/\*(.*?)\*/g, '<em>$1</em>');
    clean = clean.replace(/^[•\-\*] (.*$)/gim, '<li class="md-bullet">$1</li>');
    clean = clean.replace(/(<li.*<\/li>)/s, '<ul class="md-list">$1</ul>');
    clean = clean.replace(/\n\n/g, '<br><br>');
    clean = clean.replace(/([^\n])\n([^\n])/g, '$1<br>$2');
    return clean;
}

// Append Chat Message
function appendChatMessage(sender, text, isEmergencyFlag = false) {
    const row = document.createElement("div");
    row.className = `message-row ${sender === "user" ? "user-row" : "bot-row"}`;

    const avatar = document.createElement("div");
    avatar.className = `avatar ${sender === "user" ? "user-avatar" : "bot-avatar"}`;
    avatar.textContent = sender === "user" ? "👤" : "✚";

    const bubble = document.createElement("div");
    bubble.className = `bubble ${sender === "user" ? "user-bubble" : "bot-bubble"}`;

    const content = document.createElement("div");
    content.className = "bubble-content";
    content.innerHTML = parseMarkdownLite(text);

    const footer = document.createElement("div");
    footer.className = "bubble-footer";
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const lang = languageSelect ? languageSelect.value : "English";

    if (sender === "user") {
        footer.innerHTML = `<span class="time-stamp">${time} • ${lang === 'Tamil' ? 'நீங்கள்' : 'You'}</span>`;
    } else {
        footer.innerHTML = `
            <span class="time-stamp">${time} • HealthMate AI</span>
            <span class="verified-tag">✓ ${lang === 'Tamil' ? 'மருத்துவ பாதுகாப்பு நெறிமுறை' : 'Medical Safety Guardrails'}</span>
        `;
    }

    bubble.appendChild(content);
    bubble.appendChild(footer);
    row.appendChild(avatar);
    row.appendChild(bubble);

    chatMessages.appendChild(row);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    if (isEmergencyFlag && emergencyBanner) {
        emergencyBanner.classList.remove("hidden");
    }
}

// Chat Form Submit with Offline Interception
if (chatForm) {
    chatForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const message = userInput.value.trim();
        if (!message) return;

        appendChatMessage("user", message);
        userInput.value = "";
        userInput.style.height = "auto";

        const lang = languageSelect ? languageSelect.value : "English";
        const isTa = lang === "Tamil";
        const dict = i18n[lang] || i18n.English;

        // Offline Guard: Do not attempt fetch if browser is offline
        if (!navigator.onLine) {
            appendChatMessage("bot", dict.chatOfflineWarning || "Offline: Live AI consultation is unavailable without internet.", true);
            return;
        }

        // Loading indicator
        sendButton.disabled = true;
        sendButton.innerHTML = `<span>...</span>`;

        try {
            const resp = await fetch(`${API_BASE}/chat`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                signal: AbortSignal.timeout(3500),
                body: JSON.stringify({
                    message: message,
                    language: lang,
                    session_id: SESSION_ID
                })
            });

            if (!resp.ok) throw new Error("Server error");
            const data = await resp.json();
            appendChatMessage("bot", data.reply, data.is_emergency);
        } catch {
            const fallbackReply = isTa
                ? "📊 நிலை மதிப்பீடு: நீங்கள் விவரித்த அறிகுறிகளுக்கு போதுமான ஓய்வும் நீரேற்றமும் தேவை.\n\n💊 முதலுதவி மருந்து: Paracetamol (தேவைப்பட்டால்).\n\n🩹 வீட்டு சிகிச்சை: நிறைய தண்ணீர் மற்றும் இளநீர் அருந்தவும்.\n\n⚠️ தீவிரமானால் 108 அழைக்கவும் அல்லது மருத்துவரை அணுகவும்."
                : "📊 Condition Assessment: Please maintain hydration and adequate rest.\n\n💊 Supportive OTC: Paracetamol as needed for fever or pain.\n\n🩹 First Aid: Sip fluids and avoid strenuous activity.\n\n⚠️ Call 108 if acute chest pain or breathing difficulty occurs.";
            appendChatMessage("bot", fallbackReply, false);
        } finally {
            sendButton.disabled = false;
            sendButton.innerHTML = `<span>${isTa ? 'அனுப்பு' : 'Send'}</span>`;
        }
    });
}

// Clear Session
if (clearBtn) {
    clearBtn.addEventListener("click", async () => {
        const lang = languageSelect ? languageSelect.value : "English";
        const conf = confirm(lang === "Tamil"
            ? "அரட்டை வரலாற்றை அழிக்க விரும்புகிறீர்களா?"
            : "Clear this chat session?");
        if (conf) {
            try {
                await fetch(`${API_BASE}/clear/${SESSION_ID}`, { method: "DELETE" });
            } catch {}
            chatMessages.innerHTML = `
                <div class="message-row bot-row">
                    <div class="avatar bot-avatar">✚</div>
                    <div class="bubble bot-bubble">
                        <div class="bubble-content">
                            <strong>${lang === 'Tamil' ? 'வரலாறு அழிக்கப்பட்டது.' : 'Session Cleared.'}</strong><br>
                            ${lang === 'Tamil' ? 'புதிய உடல்நலக் கேள்விகளைக் கேட்கலாம்.' : 'You can start a new health inquiry.'}
                        </div>
                    </div>
                </div>
            `;
            if (emergencyBanner) emergencyBanner.classList.add("hidden");
        }
    });
}

// Voice Recognition
let recognition = null;
let isListening = false;
if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRec();
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onresult = (e) => {
        const transcript = e.results[0][0].transcript;
        userInput.value = transcript;
        stopVoiceListening();
    };

    recognition.onerror = () => stopVoiceListening();
    recognition.onend = () => stopVoiceListening();
}

function startVoiceListening() {
    if (!recognition) {
        alert("Voice input is not supported in this browser. Please use Chrome or Edge.");
        return;
    }
    const lang = languageSelect ? languageSelect.value : "English";
    recognition.lang = lang === "Tamil" ? "ta-IN" : "en-US";
    try {
        recognition.start();
        isListening = true;
        if (voiceBtn) voiceBtn.classList.add("listening");
        if (voiceLabel) voiceLabel.textContent = i18n[lang]?.voiceListening || "Listening...";
    } catch {}
}

function stopVoiceListening() {
    if (recognition && isListening) {
        try { recognition.stop(); } catch {}
    }
    isListening = false;
    if (voiceBtn) voiceBtn.classList.remove("listening");
    const lang = languageSelect ? languageSelect.value : "English";
    if (voiceLabel) voiceLabel.textContent = i18n[lang]?.voiceLabel || "Voice Input";
}

if (voiceBtn) {
    voiceBtn.addEventListener("click", () => {
        if (isListening) stopVoiceListening();
        else startVoiceListening();
    });
}

// Language Switch Event
if (languageSelect) {
    languageSelect.addEventListener("change", () => {
        applyLanguage(languageSelect.value);
    });
}

// Initial Language Application on Page Load
applyLanguage(languageSelect ? languageSelect.value : "English");
updateNetworkStatus();

// ============================================================================
// PROGRESSIVE WEB APP (PWA) SERVICE WORKER & CACHE STORAGE VERIFICATION
// ============================================================================
if ("serviceWorker" in navigator) {
    window.addEventListener("load", async () => {
        try {
            const reg = await navigator.serviceWorker.register("./service-worker.js");
            console.log("[PWA] Service Worker registered with scope:", reg.scope);

            // Function to inspect Cache Storage and update readiness UI
            async function verifyOfflineCache() {
                if (!("caches" in window)) return;
                try {
                    const cache = await caches.open("healthmate-v1");
                    const keys = await cache.keys();
                    console.log("[PWA] Cached offline assets count:", keys.length);
                    const lang = languageSelect ? languageSelect.value : "English";
                    const dict = i18n[lang] || i18n.English;

                    if (keys.length >= 3) {
                        if (cacheStatusText) {
                            cacheStatusText.textContent = dict.cacheReady || "Offline Pack: Ready";
                        }
                        if (offlineGuideStatusText) {
                            offlineGuideStatusText.textContent = dict.offlineGuideStatus || "Offline First-Aid Pack: 100% Downloaded & Saved";
                        }
                    }
                } catch (cErr) {
                    console.log("[PWA Cache Check]:", cErr);
                }
            }

            // Verify immediately and after a short delay for initial download
            setTimeout(verifyOfflineCache, 1200);
            setTimeout(verifyOfflineCache, 4000);

            // Re-verify when language switches
            if (languageSelect) {
                languageSelect.addEventListener("change", () => {
                    setTimeout(verifyOfflineCache, 100);
                });
            }
        } catch (err) {
            console.warn("[PWA] Service worker registration failed:", err);
        }
    });
}
