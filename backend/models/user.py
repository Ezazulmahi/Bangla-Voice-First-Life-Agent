import enum

from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String, func

from database import Base


class PreferredLanguage(str, enum.Enum):
    bn = "bn"
    en = "en"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    phone_number = Column(String(20), unique=True, nullable=False, index=True)
    # Consent to persist recorded audio (voice notes) rather than discard after processing.
    audio_retention_opt_in = Column(Boolean, nullable=False, default=False)
    # Language the agent should reply in (voice + text). Speech input stays
    # auto-detected regardless — this only affects output.
    preferred_language = Column(Enum(PreferredLanguage), nullable=False, default=PreferredLanguage.bn)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
