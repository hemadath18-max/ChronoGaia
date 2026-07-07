import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI(title="ChronoGaia Core Engine")

# Allow cross-origin connection sharing for mobile browsers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to the AI API key stored securely in your Vercel settings
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Data Validation Models
class AIDoubtRequest(BaseModel):
    current_era: str
    user_doubt: str

# Render the frontend interface on your primary link
@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    index_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as file:
            return file.read()
    return """
    <div style='color:#00ffcc; background:#020208; height:100vh; display:flex; 
    align-items:center; justify-content:center; font-family:monospace;'>
    <h3>CHRONOGAIA ERROR: index.html file not found in repository root.</h3>
    </div>
    """

# Live AI Query Resolver Route
@app.post("/api/ai/resolve-doubt")
def resolve_historical_doubt(data: AIDoubtRequest):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="AI Key not configured.")
        
    system_instruction = (
        f"You are the central core brain of ChronoGaia, an interactive app displaying Earth timeline history "
        f"and plant evolution. The user is browsing the era: {data.current_era}. "
        f"Provide a scientifically precise, grounded answer to their question. Keep it concise."
    )
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash', generation_config={"temperature": 0.3})
        prompt = f"{system_instruction}\n\nUser Question: {data.user_doubt}"
        response = model.generate_content(prompt)
        return {"ai_response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
