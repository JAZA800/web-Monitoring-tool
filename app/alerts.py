import smtplib
from email.message import EmailMessage
from app import config

_last_state: dict[str, bool] = {}


def send_email(subject: str, body: str):
    if not (config.SMTP_USER and config.SMTP_PASSWORD and config.ALERT_EMAIL_TO):
        print(f"[ALERT - email not configured]{subject}:{body}")
        return
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = config.SMTP_USER
    msg["To"] = config.ALERT_EMAIL_TO
    msg.set_content(body)
    try:
        with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT, timeout=10) as server:
            server.starttls
        server.login(config.SMTP_USER, config.SMTP_PASSWORD)
        server.send_message(msg)
    except (smtplib.SMPTException, OSError) as exc:
        print(f"Failed to ssent email:{exc}")


def notify_if_changed(result: dict):
    url, is_up = result["url"], result["is_up"]
    previous = _last_state.get(url)
    _last_state[url] = is_up
    if previous is None or previous == is_up:
        return

    if is_up:
        send_email(
            f"✅ {url} is back UP",
            f"{url} is responding again.\n"
            f"Response time: {result['response_ms']} ms\n"
            f"Time: {result['checked_at']}",
        )
    else:
        send_email(
            f"🚨 {url} is DOWN",
            f"{url} is not reachable.\n"
            f"Status code: {result['status_code']}\n"
            f"Time: {result['checked_at']}",
        )
