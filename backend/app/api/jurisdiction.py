from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.jurisdiction import Jurisdiction
from app.schemas.jurisdiction import JurisdictionCreate, JurisdictionResponse

router = APIRouter(prefix="/jurisdictions", tags=["Jurisdictions"])


@router.post("", response_model=JurisdictionResponse, status_code=201)
def create_jurisdiction(jurisdiction: JurisdictionCreate, db: Session = Depends(get_db)):
    existing = db.query(Jurisdiction).filter(Jurisdiction.name == jurisdiction.name).first()
    if existing:
        raise HTTPException(status_code=409, detail="Jurisdiction already exists")
    db_jurisdiction = Jurisdiction(**jurisdiction.model_dump())
    db.add(db_jurisdiction)
    db.commit()
    db.refresh(db_jurisdiction)
    return db_jurisdiction


@router.get("", response_model=list[JurisdictionResponse])
def get_jurisdictions(db: Session = Depends(get_db)):
    return db.query(Jurisdiction).all()