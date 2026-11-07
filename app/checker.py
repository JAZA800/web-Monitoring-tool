import time
from datetime import datetime, timezone

import requests

from app import config


def check_site(url: str) -> dict:
    start = time.perf_counter()
    status_code = None
    is_up = False
    try:
        resp = requests.get(url, timeout=config.REQUEST_TIMEOUT)
        status_code = resp.status_code
        is_up = resp.status_code < 400
    except requests.RequestException:
        pass
    response_ms = round((time.perf_counter() - start) * 1000, 2)
    return {
        "url": url,
        "status_code": status_code,
        "response_ms": response_ms,
        "is_up": is_up,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }
