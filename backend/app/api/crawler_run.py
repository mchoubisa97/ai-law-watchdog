from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.crawler_run_schema import CrawlerRunResponse
from app.services.crawler_run_service import get_all_crawler_runs, get_failed_crawler_runs

router = APIRouter(prefix="/crawler-runs", tags=["Crawler Runs"])


@router.get("", response_model=list[CrawlerRunResponse])
def fetch_crawler_runs(
    status: str = Query(None, description="Filter by status: success | failed"),
    limit: int = Query(50),
    db: Session = Depends(get_db)
):
    if status == "failed":
        return get_failed_crawler_runs(db, limit=limit)
    return get_all_crawler_runs(db, limit=limit)
