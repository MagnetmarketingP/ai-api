from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

app = FastAPI(title="AI Coach API")

# ---- Optional simple auth ----
SECRET = ""  # put a value if you want header protection

# ---- Payload models to match what Deluge sends ----
class Note(BaseModel):
    Note_Title: Optional[str] = None
    Note_Content: Optional[str] = None
    Created_Time: Optional[str] = None

class Activity(BaseModel):
    Subject: Optional[str] = None
    Description: Optional[str] = None
    Activity_Type: Optional[str] = None
    Created_Time: Optional[str] = None

class Payload(BaseModel):
    module: str
    record_id: Any
    fields: Dict[str, Any]
    activities: List[Activity] = []
    notes: List[Note] = []

@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.now(timezone.utc).isoformat()}

@app.post("/next_action")
def next_action(payload: Payload, x_auth_token: Optional[str] = Header(default=None)):
    # Optional auth
    if SECRET and x_auth_token != SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # --- VERY SIMPLE MVP LOGIC (safe to replace later) ---
    stage = payload.fields.get("Stage") or payload.fields.get("Deal_Stage") or "Unknown"
    # Dummy scores
    win = 70 if str(stage).lower() in ("qualified", "proposal sent", "quote sent") else 55
    urgency = 60

    objections = ["price"] if "price" in (str(payload.notes) + str(payload.activities)).lower() else []

    # Pick a channel
    next_channel = "Call"
    if payload.fields.get("Email_Opt_Out") is False:
        next_channel = "Email"

    summary = [
        f"Stage: {stage}",
        "Days since last touch: n/a (MVP)",
        f"Objections: {', '.join(objections) if objections else 'none detected'}"
    ]

    return {
        "win_score": win,
        "urgency": urgency,
        "objections": objections,  # list (works with multi-select)
        "next_action": {"channel": next_channel, "when": "today 6:15pm", "angle": "bill-swap framing"},
        "summary": summary,
        "sms": "Hi {{First_Name}}, quick next step to make solar easy. Have 10 mins later today? – {{Rep}}",
        "email": "Subject: Next step on your solar quote\n\nHi {{First_Name}}, quick summary above. Can we lock a 10-min slot today/tomorrow?\n\nCheers,\n{{Rep}}",
        "call_open": "Hey {{First_Name}}, 60 seconds to sanity-check the numbers and next step?"
    }
@app.get("/")
def root():
    return {
        "message": "AI API is live",
        "try": {
            "health": "/health",
            "docs": "/docs",
            "next_action": "POST /next_action"
        }
    }
