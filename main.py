
from fastapi import FastAPI

app = FastAPI()

@app.post("/next_action")
async def next_action(data: dict):
    # Example scoring logic for MVP
    return {
        "win_score": 85,
        "urgency": "high",
        "next_action": {"channel": "Phone Call"},
        "objections": ["price", "partner approval"],
        "summary": ["Stage: Proposal Sent", "Days since last touch: 7", "Objections: price, partner approval"],
        "sms": "Hi {{First_Name}}, just following up on your solar quote. Let’s confirm the best next step today. – {{Rep}}",
        "email": "Subject: Next steps on your solar quote\n\nHi {{First_Name}},\n\nHere’s a quick summary of where we’re at. I recommend a short call to confirm numbers and timing. Would today 6pm suit?\n\nCheers,\n{{Rep}}",
        "call_open": "Hey {{First_Name}}, can I take 60 seconds to review the quote and next steps with you?"
    }
