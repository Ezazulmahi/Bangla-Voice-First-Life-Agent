from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from agents.tools.complaint_draft import generate_and_save
from database import get_db
from deps import get_current_user
from models import MobilePackage, User
from schemas.complaint import ComplaintDraftIn, ComplaintDraftOut
from schemas.mobile_package import MobilePackageOut

router = APIRouter(prefix="/tools", tags=["tools"])


@router.get("/mobile-packages", response_model=list[MobilePackageOut])
def list_mobile_packages(
    max_price: float | None = Query(default=None),
    operator: str | None = Query(default=None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(MobilePackage)
    if max_price is not None:
        query = query.filter(MobilePackage.price_bdt <= max_price)
    if operator is not None:
        query = query.filter(MobilePackage.operator == operator)
    return query.order_by(MobilePackage.price_bdt.asc()).all()


@router.post("/complaint-draft", response_model=ComplaintDraftOut)
def create_complaint_draft(
    payload: ComplaintDraftIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return generate_and_save(db, payload.company_name, payload.issue_description)
