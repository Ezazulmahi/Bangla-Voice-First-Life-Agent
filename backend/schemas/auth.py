from pydantic import BaseModel, Field


class RequestOtpIn(BaseModel):
    phone_number: str = Field(min_length=6, max_length=20)


class RequestOtpOut(BaseModel):
    message: str
    debug_code: str | None = None


class VerifyOtpIn(BaseModel):
    phone_number: str = Field(min_length=6, max_length=20)
    code: str = Field(min_length=6, max_length=6)


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    phone_number: str
    audio_retention_opt_in: bool

    class Config:
        from_attributes = True
