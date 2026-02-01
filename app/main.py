from fastapi import FastAPI, Request
from app.api.honeypot import honeypot_endpoint

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Agentic Honeypot running"}

# 👇 THIS IS THE CRITICAL PART
@app.post("/")
async def guvi_entrypoint(request: Request):
    return await honeypot_endpoint(request)
