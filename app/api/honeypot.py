from fastapi import APIRouter, HTTPException, Request
import os

from app.core.memory import get_history, add_message
from app.core.detector import detect_scam
from app.core.agent import agent_reply, AgentState
from app.extraction.extractor import extract_intelligence

router = APIRouter()

# ---------------- HEALTH CHECK (GUVI USES THIS) ----------------
@router.get("/honeypot")
async def honeypot_health():
    return {
        "status": "ok",
        "message": "Agentic Honeypot endpoint is live"
    }

# ---------------- MAIN ENDPOINT ----------------
@router.post("/honeypot")
async def honeypot_endpoint(request: Request):
    # ---------- AUTH ----------
    api_key = os.environ.get("API_KEY")
    auth = (
        request.headers.get("authorization")
        or request.headers.get("Authorization")
        or request.headers.get("x-api-key")
        or request.headers.get("X-API-Key")
    )

    if not api_key:
        raise HTTPException(status_code=500, detail="API_KEY not set")

    if auth != f"Bearer {api_key}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    # ---------- SAFE BODY PARSING ----------
    try:
        body = await request.json()
    except Exception:
        body = None

    # ---------- NO BODY (GUVI TESTER CASE) ----------
    if not body:
        return {
            "is_scam": False,
            "agent_active": False,
            "reply": "Honeypot active",
            "engagement_turns": 0,
            "extracted_intelligence": {
                "upi_ids": [],
                "bank_accounts": [],
                "ifsc_codes": [],
                "phishing_urls": []
            }
        }

    message = body.get("message")
    conversation_id = body.get("conversation_id", "default")

    # ---------- EMPTY MESSAGE ----------
    if not message or message.strip() == "":
        history = get_history(conversation_id)
        return {
            "is_scam": False,
            "agent_active": False,
            "reply": "Could you please provide more details?",
            "engagement_turns": len(history),
            "extracted_intelligence": {
                "upi_ids": [],
                "bank_accounts": [],
                "ifsc_codes": [],
                "phishing_urls": []
            }
        }

    # ---------- PROCESS MESSAGE ----------
    add_message(conversation_id, "scammer", message)
    history = get_history(conversation_id)

    is_scam = detect_scam(message)

    if is_scam:
        state = AgentState.ENGAGE if len(history) <= 1 else AgentState.EXTRACT
        reply = agent_reply(state, len(history))
        intel = extract_intelligence(message)
        agent_active = True
    else:
        reply = "Okay, please continue."
        intel = {
            "upi_ids": [],
            "bank_accounts": [],
            "ifsc_codes": [],
            "phishing_urls": []
        }
        agent_active = False

    add_message(conversation_id, "agent", reply)

    return {
        "is_scam": is_scam,
        "agent_active": agent_active,
        "reply": reply,
        "engagement_turns": len(history),
        "extracted_intelligence": intel
    }
