/**
 * HealthMate AI - Minimal Client Script
 * Strictly for Browser Web APIs:
 * 1. Web Speech API (Voice input in Tamil / English)
 * 2. Chart.js Interactive Vitals Canvas
 * 3. Service Worker PWA Offline Caching
 * 4. Pain slider & utility interactions
 */

// 1. Suggestion Chip Fill & Send
function fillAndSendChat(text) {
    const input = document.getElementById('user-input');
    const form = document.getElementById('chat-form');
    if (input && form) {
        input.value = text.trim();
        form.submit();
    }
}

// 2. Pain Slider Badge Display
function updatePainDisplay(val, lang) {
    const badge = document.getElementById('pain-val-badge');
    if (!badge) return;
    const isTa = lang === 'Tamil';
    let text = isTa ? '0 - வலி இல்லை 😊' : '0 - No Pain 😊';
    const v = parseInt(val, 10);
    if (v >= 1 && v <= 3) text = isTa ? ${v} - லேசான வலி 😐 : ${v} - Mild Pain 😐;
    else if (v >= 4 && v <= 6) text = isTa ? ${v} - மிதமான வலி 😣 : ${v} - Moderate Pain 😣;
    else if (v >= 7 && v <= 9) text = isTa ? ${v} - கடுமையான தீவிர வலி 😫 : ${v} - Severe Pain 😫;
    else if (v === 10) text = isTa ? '10 - தாங்க முடியாத உச்சகட்ட வலி 🚨' : '10 - Extreme Worst Pain 🚨';
    badge.textContent = text;
}

// 3. Copy Medicine Checklist
function copyMedicineList() {
    const cards = document.querySelectorAll('.med-card');
    let text = '🏥 HealthMate AI - Essential Medicine Checklist\n\n';
    cards.forEach(c => {
        const name = c.querySelector('.med-name')?.textContent || '';
        const usage = c.querySelector('.med-row span')?.textContent || '';
        text += • : \n;
    });
    navigator.clipboard.writeText(text).then(() => {
        alert('📋 Medicine checklist copied to clipboard!');
    }).catch(() => {
        alert('Could not access clipboard.');
    });
}

// 4. Web Speech API (Voice Typing in Tamil / English)
let recognition = null;
let isListening = false;
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRec();
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onresult = (e) => {
        const transcript = e.results[0][0].transcript;
        const input = document.getElementById('user-input');
        if (input) input.value = transcript;
        stopVoiceListening();
    };
    recognition.onerror = () => stopVoiceListening();
    recognition.onend = () => stopVoiceListening();
}

function startVoiceListening() {
    if (!recognition) {
        alert('Voice recognition not supported in this browser. Please use Chrome or Edge.');
        return;
    }
    const langSelect = document.getElementById('language');
    const isTa = langSelect ? langSelect.value === 'Tamil' : false;
    recognition.lang = isTa ? 'ta-IN' : 'en-US';
    try {
        recognition.start();
        isListening = true;
        const voiceBtn = document.getElementById('voice-btn');
        const voiceLabel = document.getElementById('voice-label');
        if (voiceBtn) voiceBtn.classList.add('listening');
        if (voiceLabel) voiceLabel.textContent = isTa ? 'கேட்கிறது...' : 'Listening...';
    } catch (e) {}
}

function stopVoiceListening() {
    if (recognition && isListening) {
        try { recognition.stop(); } catch (e) {}
    }
    isListening = false;
    const voiceBtn = document.getElementById('voice-btn');
    const voiceLabel = document.getElementById('voice-label');
    const langSelect = document.getElementById('language');
    const isTa = langSelect ? langSelect.value === 'Tamil' : false;
    if (voiceBtn) voiceBtn.classList.remove('listening');
    if (voiceLabel) voiceLabel.textContent = isTa ? 'குரல் வழி உள்ளீடு' : 'Voice Input';
}

const voiceToggleBtn = document.getElementById('voice-btn');
if (voiceToggleBtn) {
    voiceToggleBtn.addEventListener('click', () => {
        if (isListening) stopVoiceListening();
        else startVoiceListening();
    });
}

// 5. Interactive Chart.js Rendering
let vitalsChartInstance = null;
let currentChartType = 'bp';

function switchChartType(type) {
    currentChartType = type;
    document.querySelectorAll('.chart-switch-btn').forEach(b => {
        b.classList.toggle('active', b.getAttribute('data-chart') === type);
    });
    fetchAndRenderChart();
}

async function fetchAndRenderChart() {
    const canvas = document.getElementById('vitalsChart');
    if (!canvas || typeof Chart === 'undefined') return;

    try {
        const resp = await fetch('/api/health-logs');
        if (!resp.ok) return;
        const json = await resp.json();
        const logs = (json.logs || []).slice().reverse(); // Chronological
        if (logs.length === 0) return;

        const langSelect = document.getElementById('language');
        const isTa = langSelect ? langSelect.value === 'Tamil' : false;
        const labels = logs.map(l => l.date ? l.date.substring(5) : '');

        let datasets = [];
        if (currentChartType === 'bp') {
            datasets = [
                {
                    label: isTa ? 'சிஸ்டாலிக் BP (mmHg)' : 'Systolic BP (mmHg)',
                    data: logs.map(l => l.systolic_bp || null),
                    borderColor: '#dc2626',
                    backgroundColor: 'rgba(220, 38, 38, 0.1)',
                    tension: 0.3,
                    borderWidth: 2,
                    spanGaps: true
                },
                {
                    label: isTa ? 'டயஸ்டாலிக் BP (mmHg)' : 'Diastolic BP (mmHg)',
                    data: logs.map(l => l.diastolic_bp || null),
                    borderColor: '#2563eb',
                    backgroundColor: 'rgba(37, 99, 235, 0.1)',
                    tension: 0.3,
                    borderWidth: 2,
                    spanGaps: true
                }
            ];
        } else if (currentChartType === 'sugar-temp') {
            datasets = [
                {
                    label: isTa ? 'இரத்த சர்க்கரை (mg/dL)' : 'Blood Sugar (mg/dL)',
                    data: logs.map(l => l.blood_glucose || null),
                    borderColor: '#7c3aed',
                    backgroundColor: 'rgba(124, 58, 237, 0.1)',
                    tension: 0.3,
                    borderWidth: 2,
                    spanGaps: true
                },
                {
                    label: isTa ? 'உடல் வெப்பநிலை (°F)' : 'Temperature (°F)',
                    data: logs.map(l => l.temperature || null),
                    borderColor: '#ea580c',
                    backgroundColor: 'rgba(234, 88, 12, 0.1)',
                    tension: 0.3,
                    borderWidth: 2,
                    spanGaps: true
                }
            ];
        } else if (currentChartType === 'pulse-spo2') {
            datasets = [
                {
                    label: isTa ? 'நாடித் துடிப்பு (BPM)' : 'Heart Rate / Pulse (BPM)',
                    data: logs.map(l => l.heart_rate || null),
                    borderColor: '#16a34a',
                    backgroundColor: 'rgba(22, 163, 74, 0.1)',
                    tension: 0.3,
                    borderWidth: 2,
                    spanGaps: true
                },
                {
                    label: isTa ? 'ஆக்சிஜன் SpO2 (%)' : 'Oxygen SpO2 (%)',
                    data: logs.map(l => l.spo2 || null),
                    borderColor: '#0a8a6b',
                    backgroundColor: 'rgba(10, 138, 107, 0.1)',
                    tension: 0.3,
                    borderWidth: 2,
                    spanGaps: true
                }
            ];
        }

        if (vitalsChartInstance) vitalsChartInstance.destroy();
        vitalsChartInstance = new Chart(canvas, {
            type: 'line',
            data: { labels, datasets },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'top', labels: { boxWidth: 14, font: { family: 'Inter', size: 11 } } }
                },
                scales: {
                    x: { grid: { color: '#f1f5f9' } },
                    y: { grid: { color: '#f1f5f9' } }
                }
            }
        });
    } catch (e) {}
}

// 6. Network & Offline Listeners
function syncNetworkUI() {
    const isOnline = navigator.onLine;
    const netBadge = document.getElementById('network-status');
    const netText = document.getElementById('network-status-text');
    const offBanner = document.getElementById('offline-banner');

    if (netBadge && netText) {
        if (isOnline) {
            netBadge.className = 'status-badge status-online-badge';
            netText.textContent = 'Online';
        } else {
            netBadge.className = 'status-badge status-offline-badge';
            netText.textContent = 'Offline Mode';
        }
    }
    if (offBanner) {
        if (isOnline) offBanner.classList.add('hidden');
        else offBanner.classList.remove('hidden');
    }
}
window.addEventListener('online', syncNetworkUI);
window.addEventListener('offline', syncNetworkUI);

// 7. Auto-scroll chat to bottom & Init on Load
window.addEventListener('DOMContentLoaded', () => {
    syncNetworkUI();
    fetchAndRenderChart();

    const chatMessages = document.getElementById('chat-messages');
    if (chatMessages) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    const textarea = document.getElementById('user-input');
    if (textarea) {
        textarea.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                document.getElementById('chat-form')?.submit();
            }
        });
    }
});

// 8. Service Worker Registration for Offline Capabilities
if ('serviceWorker' in navigator) {
    window.addEventListener('load', async () => {
        try {
            await navigator.serviceWorker.register('/static/service-worker.js');
        } catch (e) {}
    });
}
