from fastapi import FastAPI, Request, HTTPException
import os

app = FastAPI()

@app.post("/")
async def root_post(request: Request):
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

    return {
        "status": "ok",
        "honeypot_active": True,
        "secured": True,
        "message": "Honeypot endpoint validated successfully"
    }


@app.get("/")
async def root_get():
    return {
        "status": "ok",
        "message": "Agentic Honeypot service running"
    }
