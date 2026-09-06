from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from config import settings
from database import get_db
from deps import get_current_user
from models import OtpCode, User
from schemas.auth import RequestOtpIn, RequestOtpOut, TokenOut, UserOut, VerifyOtpIn
from security import create_access_token, generate_otp, hash_otp

router = APIRouter(prefix="/auth", tags=["auth"])

OTP_TTL_MINUTES = 5
MAX_OTP_ATTEMPTS = 5


@router.post("/request-otp", response_model=RequestOtpOut)
def request_otp(payload: RequestOtpIn, db: Session = Depends(get_db)):
    code = generate_otp()
    otp = OtpCode(
        phone_number=payload.phone_number,
        code_hash=hash_otp(code),
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=OTP_TTL_MINUTES),
    )
    db.add(otp)
    db.commit()

    # No SMS gateway is wired up yet, so the code is only ever logged server-side.
    print(f"[Sohai OTP] {payload.phone_number} -> {code}")

    debug_code = code if settings.env == "development" else None
    return RequestOtpOut(message="OTP sent", debug_code=debug_code)


@router.post("/verify-otp", response_model=TokenOut)
def verify_otp(payload: VerifyOtpIn, db: Session = Depends(get_db)):
    otp = (
        db.query(OtpCode)
        .filter(OtpCode.phone_number == payload.phone_number)
        .order_by(OtpCode.created_at.desc())
        .first()
    )
    if otp is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No OTP requested for this number")
    if otp.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "OTP expired, please request a new one")
    if otp.attempts >= MAX_OTP_ATTEMPTS:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Too many attempts, please request a new OTP")

    if otp.code_hash != hash_otp(payload.code):
        otp.attempts += 1
        db.commit()
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Incorrect code")

    db.delete(otp)

    user = db.query(User).filter(User.phone_number == payload.phone_number).first()
    if user is None:
        user = User(phone_number=payload.phone_number)
        db.add(user)
    db.commit()
    db.refresh(user)

    return TokenOut(access_token=create_access_token(user.id))


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user
