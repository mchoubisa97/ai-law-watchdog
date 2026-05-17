from pydantic import BaseModel


class AILawCreate(BaseModel):
    law_name: str
    jurisdiction_id: int
    category: str
    current_status: str
    official_url: str
    summary: str


class AILawResponse(BaseModel):
    id: int
    law_name: str
    jurisdiction_id: int
    category: str
    current_status: str
    official_url: str
    summary: str

    class Config:
        from_attributes = True