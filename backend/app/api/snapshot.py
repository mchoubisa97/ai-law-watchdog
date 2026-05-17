from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.source_snapshot import SourceSnapshot

router = APIRouter(prefix="/snapshots", tags=["Snapshots"])


@router.get("")
def get_snapshots(
    source_url: str = Query(None),
    law_id: int = Query(None),
    limit: int = Query(50),
    db: Session = Depends(get_db)
):
    query = db.query(SourceSnapshot)
    if source_url:
        query = query.filter(SourceSnapshot.source_url == source_url)
    if law_id:
        query = query.filter(SourceSnapshot.law_id == law_id)
    snapshots = query.order_by(SourceSnapshot.created_at.desc()).limit(limit).all()
    return [
        {
            "id": s.id,
            "law_id": s.law_id,
            "jurisdiction_id": s.jurisdiction_id,
            "source_url": s.source_url,
            "content_hash": s.content_hash,
            "created_at": s.created_at,
        }
        for s in snapshots
    ]
