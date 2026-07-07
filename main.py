import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI(title="ChronoGaia Complete Master Engine")

# Global cross-origin configuration so mobile systems connect perfectly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Core AI API Engine Handshake
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Centralized memory state tracking user sessions and playback timestamps
USER_SESSIONS = {}

# Data validation verification schemas
class UserInitRequest(BaseModel):
    device_id: str

class SyncTimelineRequest(BaseModel):
    device_id: str
    current_year_index: int
    video_timestamp_seconds: float

class AIDoubtRequest(BaseModel):
    device_id: str
    current_era: str
    user_doubt: str

# =====================================================================
# TIER 1: THE UNIFIED CYBERPUNK USER INTERFACE (SERVED ON MAIN LINK)
# =====================================================================
@app.get("/", response_class=HTMLResponse)
def serve_unified_application_hub():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>ChronoGaia Engine - Time Interface</title>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
            body, html { width: 100%; height: 100%; overflow: hidden; background-color: #020208; font-family: 'Courier New', monospace; color: #00ffcc; }
            
            /* Hyper-Realistic Viewport Mock Container */
            #viewport {
                position: absolute; top: 0; left: 0; width: 100%; height: 100%;
                background: radial-gradient(circle at center, #0a1128 0%, #020208 100%);
                display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 1; padding: 20px;
            }
            #earth-visual { font-size: 0.9rem; text-align: center; text-shadow: 0 0 8px #00ffcc; line-height: 1.6; max-width: 95%; margin-bottom: 60px; }
            
            /* Glassmorphism Cyberpunk HUD Components */
            .hud-panel { position: absolute; background: rgba(2, 2, 8, 0.85); border: 1px solid #00ffcc; box-shadow: 0 0 15px rgba(0, 255, 204, 0.2); border-radius: 6px; padding: 10px; z-index: 10; backdrop-filter: blur(8px); }
            #ticker-left { top: 15px; left: 15px; width: 52%; }
            #ticker-right { top: 15px; right: 15px; text-align: right; border-color: #ff9900; color: #ff9900; box-shadow: 0 0 15px rgba(255, 153, 0, 0.2); }
            
            /* Interactive AI Doubt Core Console Box */
            #ai-console { bottom: 125px; left: 5%; width: 90%; display: flex; border-color: #00ffcc; }
            #ai-input { flex: 1; background: transparent; border: none; color: #ffffff; font-family: inherit; padding: 8px; outline: none; font-size: 0.8rem; }
            #ai-btn { background: #00ffcc; color: #020208; border: none; padding: 0 15px; font-family: inherit; font-weight: bold; cursor: pointer; font-size: 0.8rem; }
            
            /* Haptic Scrolling Control Track */
            #controls-bottom { position: absolute; bottom: 25px; left: 5%; width: 90%; z-index: 10; }
            .label { font-size: 0.65rem; opacity: 0.7; letter-spacing: 2px; text-transform: uppercase; }
            .value { font-size: 0.95rem; font-weight: bold; margin-top: 2px; }
            input[type=range] { -webkit-appearance: none; width: 100%; background: rgba(0, 255, 204, 0.1); height: 6px; border-radius: 3px; outline: none; border: 1px solid #00ffcc; margin-top: 10px; }
            input[type=range]::-webkit-slider-thumb { -webkit-appearance: none; width: 22px; height: 22px; border-radius: 50%; background: #00ffcc; box-shadow: 0 0 10px #00ffcc; }
        </style>
    </head>
    <body>
        <div id="viewport"><div id="earth-visual">ESTABLISHING SYNCHRONIZATION WITH CLOUD DATA MATRIX...</div></div>
        <div id="ticker-left" class="hud-panel"><div class="label">AI CHRONO-STATUS</div><div id="era-val" class="value">LOADING...</div></div>
        <div id="ticker-right" class="hud-panel"><div class="label">TIMELINE YEAR</div><div id="year-val" class="value">LOADING...</div></div>
        <div id="ai-console" class="hud-panel"><input type="text" id="ai-input" placeholder="Query historical day data..."><button id="ai-btn">QUERY AI</button></div>
        <div id="controls-bottom"><div class="label" style="text-align: center;">HOLD & DRAG TO WARP PLANET HISTORY</div><input type="range" id="timeSlider" min="1" max="5" value="3" step="1"></div>

        <script>
            const slider = document.getElementById('timeSlider');
            const eraDisplay = document.getElementById('era-val');
            const yearDisplay = document.getElementById('year-val');
            const visualDisplay = document.getElementById('earth-visual');
            const aiInput = document.getElementById('ai-input');
            const aiBtn = document.getElementById('ai-btn');

            const DEVICE_ID = "chrono_mobile_user_node";
            const eraMap = { 1: "COSMIC ORIGIN", 2: "TRETA YUGA", 3: "DWAPARA YUGA", 4: "PRESENT DAY", 5: "FUTURE PROJECTION" };

            // Timeline presentation assets mapping
            const timelineData = {
                1: { era: "COSMIC ORIGIN", year: "-4.5 BILLION YRS", visual: "🌋 [LIVE ENGINE STREAM: REEL 01]<br><br>Planet forming from molten magma fields and astronomical impacts. Surface fields charging up.", defaultQuery: "Analyze atmospheric composition at birth." },
                2: { era: "TRETA YUGA", year: "7000+ BCE", visual: "🏹 [LIVE ENGINE STREAM: REEL 02]<br><br>Tracking the daily timeline of Sri Rama. Every star layout and path configuration verified.", defaultQuery: "Show me the mapping of Ram Setu construction." },
                3: { era: "DWAPARA YUGA", year: "3102 BCE", visual: "🔱 [LIVE ENGINE STREAM: REEL 03]<br><br>Tracking Sri Krishna's era. Digital sonars monitoring underwater layouts of Dwarka gates.", defaultQuery: "Show me the underwater structure of Dwarka." },
                4: { era: "PRESENT DAY", year: "2026 AD", visual: "🌍 [LIVE ENGINE STREAM: REEL 04]<br><br>Live Anthropocene satellite twin operational. Monitoring planetary terrain variance by the minute.", defaultQuery: "Show real-time global footprint expansion." },
                5: { era: "FUTURE PROJECTION", year: "+100 YEARS", visual: "🚀 [LIVE ENGINE STREAM: REEL 05]<br><br>Quantum timeline algorithm compiling the next 100 years of technology and space expansion.", defaultQuery: "Project family legacy 100 years forward." }
            };

            // Silent session registration and instant timeline positioning recall
            async function initializeUserStream() {
                try {
                    let response = await fetch('/api/user/sync-init', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ device_id: DEVICE_ID })
                    });
                    let data = await response.json();
                    slider.value = data.session_data.current_year_index;
                } catch(e) {}
                updateLocalInterface();
            }

            // Sync positioning values directly to server state cache on scroll
            async function checkpointPlaybackState(index) {
                try {
                    await fetch('/api/timeline/save-state', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            device_id: DEVICE_ID,
                            current_year_index: parseInt(index),
                            video_timestamp_seconds: index * 60.0
                        })
                    });
                } catch(e) {}
            }

            // Route dynamic doubt tracking questions up to the live AI core
            aiBtn.addEventListener('click', async () => {
                const currentEra = eraMap[slider.value];
                const userDoubt = aiInput.value;
                visualDisplay.innerHTML = "🤖 <i>COMPILING VERIFIED TRUTH DATA BLOCKS VIA CLOUD LINK...</i>";

                try {
                    let response = await fetch('/api/ai/resolve-doubt', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ device_id: DEVICE_ID, current_era: currentEra, user_doubt: userDoubt })
                    });
                    let data = await response.json();
                    visualDisplay.innerHTML = data.ai_response;
                } catch(e) {
                    visualDisplay.innerHTML = "❌ Network interface interrupted.";
                }
            });

            function updateLocalInterface() {
                const state = timelineData[slider.value];
                eraDisplay.textContent = state.era;
                yearDisplay.textContent = state.year;
                visualDisplay.innerHTML = state.visual;
                aiInput.value = state.defaultQuery;
                if (navigator.vibrate) navigator.vibrate(15);
            }

            slider.addEventListener('input', () => {
                updateLocalInterface();
                checkpointPlaybackState(slider.value);
            });

            initializeUserStream();
        </script>
    </body>
    </html>
    """

