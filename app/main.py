import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, Gauge, generate_latest

from app import config, db
from app.alerts import notify_if_changed
from app.checker import check_site

SITE_UP = Gauge("site up", "1 if the site is up , else 0", ["url"])
SITE_LATENCY = Gauge("site_response_ms", "Response time in ms", ["url"])


async def monitor_loop():
    while True:
        for url in config.SITES:
            result = await asyncio.to_thread(check_site, url)
            db.save_result(result)
            SITE_UP.labels(url=url).set(1 if result["is_up"] else 0)
            SITE_LATENCY.labels(url=url).set(result["respunse_ms"])
            await asyncio.to_thread(notify_if_changed, result)
        await asyncio.sleep(config.CHECK_INTERVAL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    task = asyncio.create_task(monitor_loop())
    yield
    task.cancel()


app = FastAPI(title="Uptime Monitor", lifespan=lifespan)


@app.get("/")
def root():
    return {"service": "uptime monitor", "sites": config.SITES}


@app.get("/status")
def status():
    return db.get_latest()


@app.get("/history")
def history(url: str, limit: int = 50):
    return db.get_history(url, limit)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
