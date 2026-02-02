from fastapi import APIRouter, Request, HTTPException
import os

router = APIRouter()

# ---------------- TESTER ENDPOINT ----------------
@router.post("/honeypot")
async def honeypot_tester(request: Request):

    api_key = os.getenv("API_KEY")

    auth = (
        request.headers.get("x-api-key")
        or request.headers.get("authorization")
        or request.headers.get("Authorization")
    )

    if not api_key:
        raise HTTPException(status_code=500, detail="API_KEY not set")

    if auth != f"Bearer {api_key}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    # ⚠️ DO NOT READ BODY
    # ⚠️ DO NOT PARSE JSON
    # ⚠️ DO NOT RUN SCAM LOGIC

    return {
        "status": "ok",
        "honeypot_active": True,
        "secured": True,
        "message": "Honeypot endpoint validated successfully"
    }
