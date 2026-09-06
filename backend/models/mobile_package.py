import enum

from sqlalchemy import Column, DateTime, Enum, Integer, Numeric, String, func

from database import Base


class Operator(str, enum.Enum):
    grameenphone = "grameenphone"
    robi = "robi"
    banglalink = "banglalink"
    airtel = "airtel"


class MobilePackage(Base):
    __tablename__ = "mobile_packages"

    id = Column(Integer, primary_key=True)
    operator = Column(Enum(Operator), nullable=False, index=True)
    name = Column(String(120), nullable=False)
    data_gb = Column(Numeric(6, 2), nullable=False)
    validity_days = Column(Integer, nullable=False)
    price_bdt = Column(Numeric(8, 2), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
