from fastapi import APIRouter, HTTPException, Request
from app.config import API_KEY
from app.schemas import HoneypotRequest
from app.core.memory import get_history, add_message
from app.core.detector import detect_scam
from app.core.agent import agent_reply, AgentState
from app.extraction.extractor import extract_intelligence

router = APIRouter()


@router.post("/honeypot")
async def honeypot_endpoint(request: Request, payload: HoneypotRequest):
    # ---------- AUTH ----------
    auth = request.headers.get("authorization") or request.headers.get("Authorization")
    if auth != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    # ---------- EMPTY MESSAGE GUARD ----------
    if payload.message is None or payload.message.strip() == "":
        history = get_history(payload.conversation_id)
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

    # ---------- STORE SCAMMER MESSAGE ----------
    add_message(payload.conversation_id, "scammer", payload.message)
    history = get_history(payload.conversation_id)

    # ---------- SCAM DETECTION ----------
    is_scam = detect_scam(payload.message)

    # ---------- AGENT LOGIC ----------
    if is_scam:
        agent_active = True

        if len(history) <= 1:
            state = AgentState.ENGAGE
        else:
            state = AgentState.EXTRACT

        reply = agent_reply(state, len(history))
        intel = extract_intelligence(payload.message)

    else:
        agent_active = False
        reply = "Okay, please continue."
        intel = {
            "upi_ids": [],
            "bank_accounts": [],
            "ifsc_codes": [],
            "phishing_urls": []
        }

    # ---------- STORE AGENT RESPONSE ----------
    add_message(payload.conversation_id, "agent", reply)

    # ---------- RESPONSE ----------
    return {
        "is_scam": is_scam,
        "agent_active": agent_active,
        "reply": reply,
        "engagement_turns": len(history),
        "extracted_intelligence": intel
    }
