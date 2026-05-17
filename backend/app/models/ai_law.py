from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class AILaw(Base):

    __tablename__ = "ai_laws"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    law_name = Column(
        String,
        nullable=False
    )

    jurisdiction_id = Column(
        Integer,
        ForeignKey("jurisdictions.id"),
        nullable=False
    )

    category = Column(String)

    current_status = Column(String)

    official_url = Column(Text)

    summary = Column(Text)

    # Relationships

    jurisdiction = relationship(
        "Jurisdiction",
        back_populates="laws"
    )

    events = relationship(
        "LawEvent",
        back_populates="law",
        cascade="all, delete"
    )

    snapshots = relationship(
        "SourceSnapshot",
        back_populates="law",
        cascade="all, delete"
    )