from typing import Optional

from sqlalchemy.orm import Session

from app.models.source_snapshot import SourceSnapshot


def get_latest_snapshot(
    db: Session,
    source_url: str
) -> Optional[SourceSnapshot]:

    return (
        db.query(SourceSnapshot)
        .filter(
            SourceSnapshot.source_url == source_url
        )
        .order_by(SourceSnapshot.created_at.desc())
        .first()
    )


def create_snapshot(
    db: Session,
    source_url: str,
    content_hash: str,
    raw_content: str,
    law_id: int = None,
    jurisdiction_id: int = None
):

    snapshot = SourceSnapshot(

        law_id=law_id,

        jurisdiction_id=jurisdiction_id,

        source_url=source_url,

        content_hash=content_hash,

        raw_content=raw_content
    )

    db.add(snapshot)

    db.commit()

    db.refresh(snapshot)

    return snapshot