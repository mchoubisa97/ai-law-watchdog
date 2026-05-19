from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import engine
from app.core.logger import logger
from app.scheduler import start_scheduler

from app.api.jurisdiction import router as jurisdiction_router
from app.api.ai_law import router as ai_law_router
from app.api.law_event import router as law_event_router
from app.api.snapshot import router as snapshot_router
from app.api.timeline import router as timeline_router
from app.api.history import router as history_router
from app.api.crawler_run import router as crawler_run_router

from app.crawlers.crawler_manager import run_all_crawlers
import app.models

app = FastAPI(
    title="AI Law Watchdog",
    description="Monitors AI regulations across global jurisdictions.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------
# Startup lifecycle
# ----------------------------
@app.on_event("startup")
def startup_event():
    logger.info("Application starting...")
    start_scheduler()


# ----------------------------
# Routers
# ----------------------------
app.include_router(jurisdiction_router)
app.include_router(ai_law_router)
app.include_router(law_event_router)
app.include_router(snapshot_router)
app.include_router(timeline_router)
app.include_router(history_router)
app.include_router(crawler_run_router)


# ----------------------------
# Health check
# ----------------------------
@app.api_route("/", methods=["GET", "HEAD"], tags=["Health"])
def root():
    return {"status": "ok", "service": "AI Law Watchdog"}


# ----------------------------
# Manual crawler trigger
# ----------------------------
@app.post("/run-crawlers", tags=["Crawlers"])
def trigger_crawlers():
    run_all_crawlers()
    return {"message": f"Crawler cycle triggered — {len(app.routes)} routes active"}
