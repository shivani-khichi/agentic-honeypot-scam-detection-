from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

API_KEY = "hackathon123"  # simple key for hackathon

@app.get("/")
def home():
    return {"message": "API is running"}

@app.post("/scam")
def scam_detector(
    data: dict,
    x_api_key: str = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    message = data.get("message", "")

    return {
        "scam_detected": True,
        "engagement": {
            "turns": 1,
            "duration_seconds": 5
        },
        "extracted_intelligence": {
            "bank_accounts": [],
            "upi_ids": [],
            "phishing_urls": []
        }
    }
