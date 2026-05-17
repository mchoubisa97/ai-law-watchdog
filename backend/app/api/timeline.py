from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.session import get_db
from app.models.source_snapshot import SourceSnapshot
from app.models.law_event import LawEvent

router = APIRouter(prefix="/timeline", tags=["Timeline"])


@router.get("")
def get_timeline(
    limit: int = Query(100, le=500),
    db: Session = Depends(get_db),
):
    snapshots = db.query(SourceSnapshot).all()
    snapshot_items = [
        {
            "type": "snapshot",
            "id": s.id,
            "law_id": s.law_id,
            "source_url": s.source_url,
            "created_at": s.created_at,
        }
        for s in snapshots
    ]

    events = db.query(LawEvent).all()
    event_items = [
        {
            "type": "event",
            "id": e.id,
            "law_id": e.law_id,
            "event_type": e.event_type,
            "description": e.description,
            "source_url": e.source_url,
            "created_at": datetime.combine(e.event_date, datetime.min.time()) if e.event_date else None,
        }
        for e in events
    ]

    combined = snapshot_items + event_items
    combined.sort(key=lambda x: x.get("created_at") or datetime.min, reverse=True)
    return combined[:limit]