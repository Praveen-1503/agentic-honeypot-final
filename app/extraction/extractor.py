import re

UPI_REGEX = r"[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}"
URL_REGEX = r"https?://[^\s]+"
BANK_ACCOUNT_REGEX = r"\b\d{9,18}\b"
IFSC_REGEX = r"\b[A-Z]{4}0[A-Z0-9]{6}\b"


def extract_intelligence(text: str):
    return {
        "upi_ids": list(set(re.findall(UPI_REGEX, text))),
        "phishing_urls": list(set(re.findall(URL_REGEX, text))),
        "bank_accounts": list(set(re.findall(BANK_ACCOUNT_REGEX, text))),
        "ifsc_codes": list(set(re.findall(IFSC_REGEX, text))),
    }
