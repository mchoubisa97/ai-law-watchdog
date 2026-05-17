from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.ai_law import AILaw
from app.schemas.ai_law import AILawCreate, AILawResponse

router = APIRouter(prefix="/ai-laws", tags=["AI Laws"])


@router.post("", response_model=AILawResponse, status_code=201)
def create_ai_law(ai_law: AILawCreate, db: Session = Depends(get_db)):
    db_ai_law = AILaw(**ai_law.model_dump())
    db.add(db_ai_law)
    db.commit()
    db.refresh(db_ai_law)
    return db_ai_law


@router.get("", response_model=list[AILawResponse])
def get_ai_laws(db: Session = Depends(get_db)):
    return db.query(AILaw).all()