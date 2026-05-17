from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.ai_law import AILaw
from app.models.source_snapshot import SourceSnapshot
from app.models.law_event import LawEvent

router = APIRouter(prefix="/history", tags=["History"])


@router.get("/{law_id}")
def get_law_history(law_id: int, db: Session = Depends(get_db)):
    law = db.query(AILaw).filter(AILaw.id == law_id).first()
    if not law:
        raise HTTPException(status_code=404, detail="Law not found")

    snapshots = (
        db.query(SourceSnapshot)
        .filter(SourceSnapshot.law_id == law_id)
        .order_by(SourceSnapshot.created_at.desc())
        .all()
    )

    events = (
        db.query(LawEvent)
        .filter(LawEvent.law_id == law_id)
        .order_by(LawEvent.event_date.desc())
        .all()
    )

    return {
        "law": {
            "id": law.id,
            "law_name": law.law_name,
            "category": law.category,
            "status": law.current_status,
            "official_url": law.official_url,
            "summary": law.summary,
        },
        "snapshots": [
            {
                "id": s.id,
                "source_url": s.source_url,
                "content_hash": s.content_hash,
                "created_at": s.created_at,
            }
            for s in snapshots
        ],
        "events": [
            {
                "id": e.id,
                "event_type": e.event_type,
                "event_date": e.event_date,
                "description": e.description,
                "source_url": e.source_url,
            }
            for e in events
        ],
        "total_snapshots": len(snapshots),
        "total_events": len(events),
    }
