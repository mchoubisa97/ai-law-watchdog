from datetime import datetime

from pydantic import BaseModel


class CrawlerRunResponse(BaseModel):

    id: int

    crawler_name: str

    status: str

    message: str | None = None

    started_at: datetime

    finished_at: datetime | None = None

    class Config:
        from_attributes = True