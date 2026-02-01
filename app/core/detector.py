SCAM_KEYWORDS = [
    "account blocked",
    "verify immediately",
    "urgent",
    "upi",
    "otp",
    "refund",
    "suspended",
    "click link",
    "kyc",
    "bank",
    "payment failed"
]


def detect_scam(message: str) -> bool:
    msg = message.lower()
    return any(keyword in msg for keyword in SCAM_KEYWORDS)
