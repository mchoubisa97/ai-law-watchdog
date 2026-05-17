from sqlalchemy import Column, Integer, String

from sqlalchemy.orm import relationship

from app.db.database import Base


class Jurisdiction(Base):

    __tablename__ = "jurisdictions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        unique=True,
        nullable=False
    )

    regulator = Column(String)

    official_source = Column(String)

    # Relationships

    laws = relationship(
        "AILaw",
        back_populates="jurisdiction",
        cascade="all, delete"
    )