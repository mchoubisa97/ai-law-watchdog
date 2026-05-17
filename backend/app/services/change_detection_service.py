"""
Deprecated: BaseCrawler now handles change detection directly.
Kept for backward compatibility only.
"""
from app.services.snapshot_service import get_latest_snapshot, create_snapshot


def create_snapshot_if_changed(
    db,
    source_url: str,
    content_hash: str,
    raw_content: str,
    law_id: int = None,
    jurisdiction_id: int = None,
):
    latest = get_latest_snapshot(db, source_url)

    if latest and latest.content_hash == content_hash:
        return {"changed": False, "snapshot": latest}

    snapshot = create_snapshot(
        db=db,
        source_url=source_url,
        content_hash=content_hash,
        raw_content=raw_content,
        law_id=law_id,
        jurisdiction_id=jurisdiction_id,
    )
    return {"changed": True, "snapshot": snapshot}
