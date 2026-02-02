from fastapi import APIRouter, HTTPException, Request
import os

router = APIRouter()


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

    # ---------- TRY TO READ BODY (OPTIONAL) ----------
    try:
        body = await request.json()
    except Exception:
        body = {}

    message = body.get("message", "")

    if not isinstance(message, str):
        message = ""

    # ---------- MINIMAL VALID RESPONSE ----------
    return {
        "is_scam": False,
        "agent_active": False,
        "reply": "Honeypot active and listening.",
        "engagement_turns": 0,
        "extracted_intelligence": {
            "upi_ids": [],
            "bank_accounts": [],
            "ifsc_codes": [],
            "phishing_urls": []
        }
    }
