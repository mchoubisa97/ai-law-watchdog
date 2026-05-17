from sqlalchemy.orm import Session

from app.models.law_event import LawEvent


def create_law_event(
    db: Session,
    law_id: int,
    event_type: str,
    description: str,
    source_url: str,
    event_date
):
    event = LawEvent(
        law_id=law_id,
        event_type=event_type,
        description=description,
        source_url=source_url,
        event_date=event_date
    )

    db.add(event)

    db.commit()

    db.refresh(event)

    return event