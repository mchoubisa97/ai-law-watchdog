from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.law_event import LawEvent
from app.schemas.law_events import LawEventCreate, LawEventResponse

router = APIRouter(prefix="/law-events", tags=["Law Events"])


@router.get("", response_model=list[LawEventResponse])
def get_law_events(
    law_id: int = Query(None),
    limit: int = Query(100),
    db: Session = Depends(get_db)
):
    query = db.query(LawEvent)
    if law_id:
        query = query.filter(LawEvent.law_id == law_id)
    return query.order_by(LawEvent.event_date.desc()).limit(limit).all()


@router.post("", response_model=LawEventResponse, status_code=201)
def create_law_event_api(payload: LawEventCreate, db: Session = Depends(get_db)):
    law_event = LawEvent(**payload.model_dump())
    db.add(law_event)
    db.commit()
    db.refresh(law_event)
    return law_event
