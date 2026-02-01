from fastapi import APIRouter, HTTPException, Request
import os
from typing import Optional

from app.schemas import HoneypotRequest
from app.core.memory import get_history, add_message
from app.core.detector import detect_scam
from app.core.agent import agent_reply, AgentState
from app.extraction.extractor import extract_intelligence

router = APIRouter()

# --------------------------------------------------
# GET → Health check (required by GUVI tester)
# --------------------------------------------------
@router.get("/honeypot")
async def honeypot_health():
    return {
        "status": "ok",
        "message": "Agentic Honeypot endpoint is live"
    }

# --------------------------------------------------
# POST → Main honeypot logic
# --------------------------------------------------
@router.post("/honeypot")
async def honeypot_endpoint(
    request: Request,
    payload: Optional[HoneypotRequest] = None
):
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

    # ---------- TESTER EMPTY BODY ----------
    if payload is None:
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

    # ---------- EMPTY MESSAGE ----------
    if not payload.message or payload.message.strip() == "":
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
        state = AgentState.ENGAGE if len(history) <= 1 else AgentState.EXTRACT
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
