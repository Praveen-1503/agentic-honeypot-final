from pydantic import BaseModel
from typing import Optional, List


class HoneypotRequest(BaseModel):
    conversation_id: str
    message: str
    timestamp: Optional[str] = None


class ExtractedIntelligence(BaseModel):
    upi_ids: List[str] = []
    bank_accounts: List[str] = []
    ifsc_codes: List[str] = []
    phishing_urls: List[str] = []


class HoneypotResponse(BaseModel):
    is_scam: bool
    agent_active: bool
    reply: str
    engagement_turns: int
    extracted_intelligence: ExtractedIntelligence
