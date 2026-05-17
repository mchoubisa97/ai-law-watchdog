from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from datetime import datetime

from app.db.database import Base


class SourceSnapshot(Base):

    __tablename__ = "source_snapshots"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    law_id = Column(
        Integer,
        ForeignKey("ai_laws.id"),
        nullable=True
    )

    jurisdiction_id = Column(
        Integer,
        ForeignKey("jurisdictions.id"),
        nullable=True
    )

    source_url = Column(
        Text,
        nullable=False
    )

    content_hash = Column(
        Text,
        nullable=False
    )

    raw_content = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    law = relationship(
        "AILaw",
        back_populates="snapshots"
    )

    jurisdiction = relationship(
        "Jurisdiction"
    )