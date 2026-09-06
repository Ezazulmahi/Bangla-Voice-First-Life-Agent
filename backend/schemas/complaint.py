from datetime import datetime

from pydantic import BaseModel


class ComplaintDraftIn(BaseModel):
    company_name: str
    issue_description: str


class ComplaintDraftOut(BaseModel):
    id: int
    company_name: str
    issue_description: str
    generated_text: str
    created_at: datetime

    class Config:
        from_attributes = True
