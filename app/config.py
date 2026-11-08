import os

SITES = [
    s.strip()
    for s in os.getenv("SITES", "https://google.com,https://github.com").split(",")
    if s.strip()
]
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "60"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))


# mongodb
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "uptime_monitor")

# emails
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
ALERT_EMAIL_TO = os.getenv("ALERT_EMAIL_TO", "")
