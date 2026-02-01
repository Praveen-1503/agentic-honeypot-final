from fastapi import FastAPI, Request
from app.api.honeypot import router as honeypot_router

app = FastAPI()

app.include_router(honeypot_router)

@app.get("/")
def root():
    return {"status": "Agentic Honeypot running"}

@app.post("/")
async def root_post(request: Request):
    return {
        "status": "ok",
        "message": "Agentic Honeypot endpoint is live"
    }
