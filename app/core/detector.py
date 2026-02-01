def detect_scam(message: str) -> bool:
    if not message:
        return False

    msg = message.lower()

    scam_keywords = [
        "account",
        "blocked",
        "suspended",
        "verify",
        "kyc",
        "urgent",
        "send money",
        "upi",
        "bank",
        "payment",
        "link",
        "click",
        "refund"
    ]

    return any(keyword in msg for keyword in scam_keywords)
