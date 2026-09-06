from sqlalchemy import Column, DateTime, Integer, String, func

from database import Base


class OtpCode(Base):
    """Short-lived phone verification codes. Auxiliary auth table, not part of
    the core product ER schema."""

    __tablename__ = "otp_codes"

    id = Column(Integer, primary_key=True)
    phone_number = Column(String(20), nullable=False, index=True)
    code_hash = Column(String(64), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    attempts = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
