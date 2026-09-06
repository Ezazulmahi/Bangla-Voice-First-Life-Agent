from datetime import datetime

from pydantic import BaseModel


class MobilePackageOut(BaseModel):
    id: int
    operator: str
    name: str
    data_gb: float
    validity_days: int
    price_bdt: float
    updated_at: datetime

    class Config:
        from_attributes = True
