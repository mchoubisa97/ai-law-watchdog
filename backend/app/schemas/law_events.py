from datetime import date
from pydantic import BaseModel
from typing import Optional


class LawEventCreate(BaseModel):
    law_id: int
    event_type: str
    event_date: date
    description: str
    source_url: Optional[str] = None


class LawEventResponse(BaseModel):
    id: int
    law_id: int
    event_type: str
    event_date: date
    description: str
    source_url: Optional[str] = None

    class Config:
        from_attributes = True