from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.honeypot import router as honeypot_router
import os

app = FastAPI()

# ---------------- GUVI SAFE ENTRYPOINT ----------------
@app.post("/")
async def guvi_root(request: Request):
    # DO NOT TOUCH BODY
    # DO NOT VALIDATE
    return JSONResponse(
        status_code=200,
        content={
            "status": "ok",
            "message": "Agentic Honeypot active"
        }
    )

@app.get("/")
async def guvi_root_get():
    return {
        "status": "ok",
        "message": "Agentic Honeypot active"
    }

# ---------------- REAL API ----------------
app.include_router(honeypot_router)
