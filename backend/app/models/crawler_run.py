from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.database import Base


class CrawlerRun(Base):

    __tablename__ = "crawler_runs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    crawler_name = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        nullable=False
    )

    message = Column(
        String,
        nullable=True
    )

    started_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    finished_at = Column(
        DateTime,
        default=datetime.utcnow
    )