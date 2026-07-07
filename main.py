import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI(title="ChronoGaia Core Engine")

# Enable global cross-origin access so your mobile client can talk to the cloud server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the Gemini AI model connection using environment variables
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("Warning: GEMINI_API_KEY environment variable not configured.")

# In-memory session database simulating instant user tracking and auto-pause positioning
USER_SESSIONS = {}

# Data validation schemas
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

@app.get("/")
def health_check():
    return {"status": "online", "engine": "ChronoGaia Core", "version": "1.0.0"}

# 1. Automatic User Entry & Sign-up Route
@app.post("/api/user/sync-init")
def sync_user_initialization(data: UserInitRequest):
    # If device is new, automatically initialize state at Earth's Birth (Index 1)
    if data.device_id not in USER_SESSIONS:
        USER_SESSIONS[data.device_id] = {
            "current_year_index": 1,
            "video_timestamp_seconds": 0.0
        }
    return {"status": "success", "session_data": USER_SESSIONS[data.device_id]}

# 2. Auto-Pause & Auto-Resume State Tracker
@app.post("/api/timeline/save-state")
def save_video_state(data: SyncTimelineRequest):
    if data.device_id not in USER_SESSIONS:
        USER_SESSIONS[data.device_id] = {}
        
    USER_SESSIONS[data.device_id]["current_year_index"] = data.current_year_index
    USER_SESSIONS[data.device_id]["video_timestamp_seconds"] = data.video_timestamp_seconds
    return {"status": "saved", "synchronized_timestamp": data.video_timestamp_seconds}

# 3. Live AI Brain Core (Resolving user doubts instantly relative to their active era)
@app.post("/api/ai/resolve-doubt")
def resolve_historical_doubt(data: AIDoubtRequest):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="AI backend orchestration layer not configured.")
        
    # Injecting systemic historical ground truth rules to guide the response context
    system_instruction = (
        f"You are the central core brain of ChronoGaia, a digital time machine mapping absolute Earth history "
        f"from formation to eventual destruction. The user is currently navigating the era: {data.current_era}. "
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
        raise HTTPException(status_code=500, detail=f"AI routing anomaly: {str(e)}")
  
