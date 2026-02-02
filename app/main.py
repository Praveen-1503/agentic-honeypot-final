from fastapi import FastAPI, Request, HTTPException
import os

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
async def root_post(request: Request):
    # Auth check
    validate_auth(request)

    # IMPORTANT: Do NOT read request.json()
    # Do NOT validate body
    return {
        "status": "ok",
        "honeypot": "active",
        "secured": True,
        "message": "Agentic Honeypot endpoint reachable"
    }


@app.get("/")
async def root_get():
    return {
        "status": "ok",
        "service": "Agentic Honeypot running"
    }
