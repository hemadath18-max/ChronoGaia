import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI(title="ChronoGaia Complete Engine")

# Universal cross-origin policy allowing local mobile clients to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Core AI Synchronization Link
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Central session manager tracking your timeline auto-pause values
USER_SESSIONS = {}

# Data Schema Definitions
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

# 1. SERVING FRONTEND INTERFACE DIRECTLY FROM THE COMPLIED APP ROOT
@app.get("/", response_class=HTMLResponse)
def serve_master_frontend():
    index_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as file:
            return file.read()
    return """
    <div style='color:#00ffcc; background:#020208; height:100vh; display:flex; 
    align-items:center; justify-content:center; font-family:monospace;'>
    <h3>CHRONOGAIA: INDEX.HTML FILE MISSING IN REPOSITORY BLOCKS</h3>
    </div>
    """

# 2. SEAMLESS AUTOMATIC USER INITIALIZATION
@app.post("/api/user/sync-init")
def sync_user_initialization(data: UserInitRequest):
    if data.device_id not in USER_SESSIONS:
        USER_SESSIONS[data.device_id] = {
            "current_year_index": 3,  # Set default start context
            "video_timestamp_seconds": 180.0
        }
    return {"status": "success", "session_data": USER_SESSIONS[data.device_id]}

# 3. LIVE POSITION STATE SAVER (AUTO-PAUSE CONTROLLER)
@app.post("/api/timeline/save-state")
def save_video_state(data: SyncTimelineRequest):
    if data.device_id not in USER_SESSIONS:
        USER_SESSIONS[data.device_id] = {}
    USER_SESSIONS[data.device_id]["current_year_index"] = data.current_year_index
    USER_SESSIONS[data.device_id]["video_timestamp_seconds"] = data.video_timestamp_seconds
    return {"status": "saved", "synchronized_timestamp": data.video_timestamp_seconds}

# 4. LIVE KNOWLEDGE CORE INTEGRATION
@app.post("/api/ai/resolve-doubt")
def resolve_historical_doubt(data: AIDoubtRequest):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="AI Brain Core access token unconfigured.")
        
    system_instruction = (
        f"You are the central core brain of ChronoGaia, a digital time machine mapping absolute Earth history "
        f"from formation to eventual destruction. The user is navigating the era: {data.current_era}. "
        f"Provide a scientifically precise, historically grounded, or archaeologically verified response. "
        f"If the user asks about the Itihasa periods (Ramayana/Krishna), cross-reference structural details "
        f"and geographical configurations accurately. Keep your response direct and punchy."
    )
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash', generation_config={"temperature": 0.3})
        prompt = f"{system_instruction}\n\nUser Question: {data.user_doubt}"
        response = model.generate_content(prompt)
        return {"status": "resolved", "ai_response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI internal stream failure: {str(e)}")
        
