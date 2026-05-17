from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    Date
)

from sqlalchemy.orm import relationship

from app.db.database import Base


class LawEvent(Base):

    __tablename__ = "law_events"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    law_id = Column(
        Integer,
        ForeignKey("ai_laws.id"),
        nullable=False
    )

    event_type = Column(String)

    event_date = Column(Date)

    description = Column(Text)

    source_url = Column(Text)

    # Relationship

    law = relationship(
        "AILaw",
        back_populates="events"
    )