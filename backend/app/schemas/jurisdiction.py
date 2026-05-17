from pydantic import BaseModel
from typing import Optional


class JurisdictionCreate(BaseModel):
    name: str
    regulator: Optional[str] = None
    official_source: Optional[str] = None


class JurisdictionResponse(BaseModel):
    id: int
    name: str
    regulator: Optional[str] = None
    official_source: Optional[str] = None

    class Config:
        from_attributes = True