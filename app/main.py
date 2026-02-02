from fastapi import FastAPI
from app.api.honeypot import router

app = FastAPI()

app.include_router(router)

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Agentic Honeypot service running"
    }
