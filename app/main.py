from fastapi import FastAPI, Request
from app.api.honeypot import honeypot_endpoint

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Agentic Honeypot running"}

# ✅ GUVI ENTRYPOINT (NO BODY EXPECTED)
@app.post("/")
async def guvi_entrypoint(request: Request):
    try:
        body = await request.json()
    except Exception:
        body = None

    return await honeypot_endpoint(
        request=request,
        payload=body
    )
