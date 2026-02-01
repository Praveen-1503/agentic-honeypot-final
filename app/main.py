from fastapi import FastAPI
from app.api.honeypot import router as honeypot_router

app = FastAPI()

app.include_router(honeypot_router)
