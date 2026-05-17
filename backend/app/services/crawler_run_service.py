from datetime import datetime
from sqlalchemy.orm import Session
from app.models.crawler_run import CrawlerRun


def create_crawler_run(
    db: Session,
    crawler_name: str,
    status: str,
    message: str = None,
    started_at: datetime = None,
    finished_at: datetime = None,
):
    run = CrawlerRun(
        crawler_name=crawler_name,
        status=status,
        message=message,
        started_at=started_at or datetime.utcnow(),
        finished_at=finished_at or datetime.utcnow(),
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


def get_all_crawler_runs(db: Session, limit: int = 50):
    return (
        db.query(CrawlerRun)
        .order_by(CrawlerRun.started_at.desc())
        .limit(limit)
        .all()
    )


def get_failed_crawler_runs(db: Session, limit: int = 50):
    return (
        db.query(CrawlerRun)
        .filter(CrawlerRun.status == "failed")
        .order_by(CrawlerRun.started_at.desc())
        .limit(limit)
        .all()
    )
