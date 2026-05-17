from pydantic import BaseModel
from datetime import datetime


class SnapshotOut(BaseModel):
    id: int
    source_url: str
    content_hash: str
    created_at: datetime

    class Config:
        from_attributes = True