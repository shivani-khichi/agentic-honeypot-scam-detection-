
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Agentic Honey-Pot API")

# 🔓 CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # frontend origin allowed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ API KEY (as your friend said)
API_KEY = "hackathon123"


# -------------------- MODELS --------------------
class MessageRequest(BaseModel):
    message: str


# -------------------- SCAM KEYWORDS --------------------
SCAM_KEYWORDS = {
    "otp_upi_bank": [
        "otp", "upi", "bank", "account", "pin", "atm", "cvv",
        "debit card", "credit card", "net banking", "passbook",
        "transaction", "payment", "blocked", "freeze"
    ],

    "lottery_prize": [
        "lottery", "lucky draw", "won", "winner", "congratulations",
        "prize", "reward", "gift", "cash prize", "jackpot",
        "you have won", "claim your prize", "claim reward"
    ],

    "kyc_verification": [
        "kyc", "verify", "verification", "update kyc",
        "aadhaar", "pan", "pan card", "link aadhaar",
        "document upload", "re-kyc"
    ],

    "phishing_links": [
        "click", "link", "http", "https", "bit.ly", "tinyurl",
        "download", "apk", "install app", "open link"
    ],

    "job_scam": [
        "job offer", "work from home", "salary", "interview",
        "registration fee", "pay first", "data entry",
        "hiring", "selected", "offer letter"
    ],

    "loan_scam": [
        "loan", "instant loan", "pre-approved", "processing fee",
        "loan approved", "pay fee", "low interest"
    ],

    "investment_crypto": [
        "crypto", "bitcoin", "trading", "investment",
        "double money", "high returns", "profit guaranteed",
        "forex"
    ],

    "courier_customs": [
        "courier", "customs", "parcel", "package", "delivery",
        "held", "blocked", "fine", "police case", "illegal item"
    ]
}


# -------------------- ROUTES --------------------
@app.get("/")
def root():
    return {"status": "API running"}


@app.post("/scam")
def scam_check(data: MessageRequest, x_api_key: str = Header(None)):
    # API Key validation
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    text = data.message.lower()

    detected_categories = []
    matched_words = []

    for category, keywords in SCAM_KEYWORDS.items():
        for word in keywords:
            if word in text:
                detected_categories.append(category)
                matched_words.append(word)

    scam = len(detected_categories) > 0

    return {
        "scam_detected": scam,
        "agent_activated": scam,
        "extracted_data": {
            "scam_categories": list(set(detected_categories)),
            "matched_words": list(set(matched_words))
        },
        "confidence_score": 0.85 if scam else 0.15
    }
