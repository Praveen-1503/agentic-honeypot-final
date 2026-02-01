def detect_scam(message):
    if not isinstance(message, str):
        return False
    msg = message.lower()

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
