
import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, Gauge, generate_latest
from pydantic import BaseModel

from app import config, db
from app.alerts import notify_if_changed
from app.checker import check_site


logger = logging.getLogger("uvicorn.error")

SITE_UP = Gauge("site_up", "1 if the site is up, else 0", ["url"])
SITE_LATENCY = Gauge("site_response_ms", "Response time in ms", ["url"])


async def monitor_loop():
    while True:
        for url in list(config.SITES):
            try:
                result = await asyncio.to_thread(check_site, url)
                db.save_result(result)

                SITE_UP.labels(url=url).set(
                    1 if result["is_up"] else 0
                )

                if result["is_up"]:
                    SITE_LATENCY.labels(url=url).set(
                        result["response_ms"]
                    )

                await asyncio.to_thread(notify_if_changed, result)

            except Exception:
                logger.exception("Check failed for %s", url)

        await asyncio.sleep(config.CHECK_INTERVAL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    task = asyncio.create_task(monitor_loop())

    yield

    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


app = FastAPI(title="Uptime Monitor", lifespan=lifespan)


@app.get("/")
def root():
    return {"service": "uptime monitor", "sites": config.SITES}


@app.get("/status")
def status():
    return db.get_latest()


@app.get("/history")
def history(url: str, limit: int = 50):
    records = db.get_history(url, limit)

    if not records:
        raise HTTPException(
            status_code=404,
            detail="No records for this URL"
        )

    return records


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )


class SiteIn(BaseModel):
    url: str


@app.get("/sites")
def list_sites():
    return config.SITES


@app.post("/sites", status_code=201)
def add_site(site: SiteIn):
    if site.url in config.SITES:
        raise HTTPException(
            status_code=400,
            detail="Site already monitored"
        )

    config.SITES.append(site.url)
    return {"sites": config.SITES}


@app.post("/check")
async def check_now(url: str):
    return await asyncio.to_thread(check_site, url)


@app.get("/summary")
def summary():
    latest = db.get_latest()
    up = sum(1 for r in latest if r["is_up"])

    return {
        "total": len(latest),
        "up": up,
        "down": len(latest) - up
    }
