from fastapi import FastAPI, Request, HTTPException, Body
import os
from typing import Dict, Any

app = FastAPI()


def validate_auth(request: Request):
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


@app.post("/")
async def honeypot_entrypoint(
    request: Request,
    body: Dict[str, Any] = Body(default={})  # ⭐ THIS IS THE KEY
):
    validate_auth(request)

    # Do NOT process body
    # Do NOT validate body
    return {
        "status": "ok",
        "honeypot": "active",
        "message": "Honeypot endpoint reachable and secured"
    }


@app.get("/")
async def health():
    return {
        "status": "ok",
        "service": "Agentic Honeypot running"
    }
