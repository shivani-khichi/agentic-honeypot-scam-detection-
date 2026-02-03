from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Agentic Honey-Pot API")

API_KEY = "test123"

class Message(BaseModel):
    sender: str
    text: str

class ScamRequest(BaseModel):
    conversation_id: str
    messages: List[Message]

@app.get("/")
def root():
    return {"status": "API running"}

@app.post("/analyze")
def analyze(data: ScamRequest, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    text = data.messages[-1].text.lower()
    scam = any(word in text for word in ["otp", "upi", "bank", "click"])

    return {
        "scam_detected": scam,
        "agent_activated": scam,
        "extracted_data": {},
        "engagement_turns": len(data.messages),
        "confidence_score": 0.8 if scam else 0.2
    }
    from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

API_KEY = "mysecretkey"   # yahi key baad me submit hogi

@app.get("/")
def home():
    return {"status": "API running"}

@app.post("/scam")
def scam_detector(data: dict, x_api_key: str = Header(None)):
    # API key check
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    message = data.get("message", "")

    return {
        "scam_detected": True,
        "extracted": {
            "upi": [],
            "account": [],
            "urls": []
        },
        "agent_reply": "Please share more details."
    }
